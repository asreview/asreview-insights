import warnings

import numpy as np
from matplotlib.ticker import MaxNLocator

from asreviewcontrib.visualization.plot_base import PlotBase


class PlotInclusions(PlotBase):
    def __init__(self, analyses, result_format="percentage", thick=None):
        """Class for the Inclusions plot.

        Plot the number of queries that turned out to be included
        in the final review.
        """
        super(PlotInclusions, self).__init__(analyses)
        self.result_format = result_format
        self.col = {}

        if thick is None:
            thick = {key: True for key in list(self.analyses)}
        self.thick = thick

        if result_format == "percentage":
            self.box_dist = 0.5
        else:
            self.box_dist = 100

        max_len = 0
        for i, data_key in enumerate(reversed(self.analyses)):
            analysis = self.analyses[data_key]

            inc_found = analysis.inclusions_found(result_format=result_format)
            n_initial = analysis.inc_found[False]["n_initial"]
            n_after_init = len(analysis.labels) - n_initial
            max_len = max(max_len, n_after_init)

            max_y = analysis.inc_found[False]["inc_after_init"]

            self.col[data_key] = "C" + str((len(self.analyses) - 1 - i) % 10)
            col = self.col[data_key]

            if self.thick[data_key]:
                lw = 2
            else:
                lw = 0.7

            myplot = self.ax.errorbar(inc_found[0], inc_found[1], color=col, lw=lw)
            if self.thick[data_key]:
                self.legend_name.append(f"{data_key}")
                self.legend_plt.append(myplot)

        # show absolute number next to percentages
        if result_format == "number":

            # duplicate x axis
            self.ax2 = self.ax.twiny()

            # top axis
            self.ax.set_xlim(0, max_len)
            self.ax.set_xlabel("# Reviewed")

            # bottom axis
            self.ax2.set_xlim(0, 100)
            self.ax2.set_xlabel("% Reviewed")

            self.ax3 = self.ax.twinx()

            # left axis
            spacing_top = 1.05
            self.ax.set_ylim(0, spacing_top * max_y)
            self.ax.set_ylabel("# Relevant records found")

            # right axis
            self.ax3.set_ylim(0, spacing_top * 100)
            self.ax3.set_ylabel("% Relevant records found")

        # only display percentage
        elif result_format == "percentage":
            self.ax.set_xlabel("% Records reviewed")
            self.ax.set_ylabel("% Relevant records found")

        # no decimals on y-axis
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        self.fig.tight_layout()

    def add_WSS(self, *args, **kwargs):  # noqa
        warnings.warn("add_WSS is deprecated, use add_wss instead",
                      DeprecationWarning)
        self.add_wss(*args, **kwargs)

    def add_wss(self,
                data_key,
                value=95,
                text_at=None,
                add_value=False,
                alpha=0.8,
                text_col="white",
                add_text=True,
                **kwargs):
        analysis = self.analyses[data_key]
        col = self.col[data_key]

        if value is None:
            return

        text = f"WSS@{value}%"
        wss_val, wss_x, wss_y = analysis.wss(value,
                                             x_format=self.result_format,
                                             **kwargs)
        if wss_x is None or wss_y is None:
            return

        if add_value:
            text += r"$\approx" + f" {round(wss_val, 2)}" + r"\%$"

        if text_at is None:
            text_at = (wss_x[0] + self.box_dist, (wss_y[0] + wss_y[1]) / 2)

        self.ax.plot(wss_x, wss_y, color=col, ls=(0, (5, 1)))
        self.ax.plot(wss_x, (0, wss_y[0]), color=col, ls=(0, (1, 5)))
        bbox = dict(boxstyle='round', facecolor=col, alpha=alpha)
        if add_text:
            self.ax.text(*text_at, text, color=text_col, bbox=bbox)

    def add_RRF(self, *args, **kwargs):  # noqa
        warnings.warn("add_RRF is deprecated, use add_rrf instead",
                      DeprecationWarning)
        self.add_rrf(*args, **kwargs)

    def add_rrf(self,
                data_key,
                value=10,
                text_at=None,
                add_value=False,
                alpha=0.8,
                text_col="white",
                add_text=True,
                **kwargs):
        analysis = self.analyses[data_key]
        col = self.col[data_key]
        if value is None:
            return

        rrf_val, rrf_x, rrf_y = analysis.rrf(value,
                                             x_format=self.result_format,
                                             **kwargs)
        if rrf_x is None or rrf_y is None:
            return

        text = f"RRF@{value}%"
        if add_value:
            text += r"$\approx" + f" {round(rrf_val, 2)}" + r"\%$"

        rrf_x = 0, rrf_x[0]
        rrf_y = rrf_y[1], rrf_y[1]
        if text_at is None:
            text_at = (rrf_x[0] + self.box_dist, rrf_y[0] * 0.9)

        self.ax.plot(rrf_x, rrf_y, color=col, ls="--")
        bbox = dict(boxstyle='round', facecolor=col, alpha=alpha)
        if add_text:
            self.ax.text(*text_at, text, color=text_col, bbox=bbox)

    def add_random(self, line_col='grey', add_text=True, text_at=None):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        if text_at is None:
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
            text_at = (
                np.average(xlim) - 0.07 * (xlim[1] - xlim[0]),
                np.average(ylim) + 0.07 * (ylim[1] - ylim[0]),
            )

        bbox = dict(boxstyle='round', facecolor='0.65')

        # add label for random line
        if add_text:
            self.ax.text(*text_at, "random", color="black", bbox=bbox)

        xlim = [max(x, 0) for x in xlim]
        if self.result_format == "percentage":
            xlim = [min(x, 100) for x in xlim]
            y_vals = xlim
        else:
            analysis = self.analyses[list(self.analyses)[0]]
            n_labels = len(analysis.labels)
            n_initial = analysis.inc_found[False]["n_initial"]
            max_y = analysis.inc_found[False]["inc_after_init"]
            label_after_init = n_labels - n_initial
            y_vals = max_y * np.array(xlim) / label_after_init
        self.ax.plot(xlim, y_vals, color=line_col, ls="--")

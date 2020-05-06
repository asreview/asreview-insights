import numpy as np

from asreviewcontrib.visualization.plot_base import PlotBase


class PlotInclusions(PlotBase):
    def __init__(self, analyses, result_format="percentage", thick=None):
        """
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

            self.col[data_key] = "C"+str((len(self.analyses)-1-i) % 10)
            col = self.col[data_key]

            if self.thick[data_key]:
                lw = 2
            else:
                lw = 0.7

            myplot = self.ax.errorbar(*inc_found, color=col, lw=lw)
            if self.thick[data_key]:
                self.legend_name.append(f"{data_key}")
                self.legend_plt.append(myplot)

        if result_format == "number":
            self.ax2 = self.ax.twiny()
            self.ax.set_xlim(0, max_len)
            self.ax2.set_xlim(0, 100)
            self.ax.set_xlabel("# Reviewed")
            self.ax2.set_xlabel("% Reviewed")
            self.ax.set_ylabel("# Inclusions found")
        elif result_format == "percentage":
            self.ax.set_xlabel("% Reviewed")
            self.ax.set_ylabel("% Inclusions found")
        self.fig.tight_layout()

    def add_WSS(self, data_key, value=95, text_at=None, add_value=False,
                alpha=0.8, text_col="white", add_text=True, **kwargs):
        analysis = self.analyses[data_key]
        col = self.col[data_key]

        if value is None:
            return

        text = f"WSS@{value}%"
        WSS_val, WSS_x, WSS_y = analysis.wss(
            value, x_format=self.result_format, **kwargs)
        if WSS_x is None or WSS_y is None:
            return

        if add_value:
            text += r"$\approx" + f" {round(WSS_val, 2)}" + r"\%$"

        if text_at is None:
            text_at = (WSS_x[0] + self.box_dist, (WSS_y[0] + WSS_y[1])/2)

        self.ax.plot(WSS_x, WSS_y, color=col, ls="--")
        self.ax.plot(WSS_x, (0, WSS_y[0]), color=col, ls=":")
        bbox = dict(boxstyle='round', facecolor=col, alpha=alpha)
        if add_text:
            self.ax.text(*text_at, text, color=text_col, bbox=bbox)

    def add_RRF(self, data_key, value=10, text_at=None, add_value=False,
                alpha=0.8, text_col="white", add_text=True, **kwargs):
        analysis = self.analyses[data_key]
        col = self.col[data_key]
        if value is None:
            return

        RRF_val, RRF_x, RRF_y = analysis.rrf(
            value, x_format=self.result_format, **kwargs)
        if RRF_x is None or RRF_y is None:
            return

        text = f"RRF@{value}%"
        if add_value:
            text += r"$\approx" + f" {round(RRF_val, 2)}" + r"\%$"

        RRF_x = 0, RRF_x[0]
        RRF_y = RRF_y[1], RRF_y[1]
        if text_at is None:
            text_at = (RRF_x[0] + self.box_dist, RRF_y[0] + self.box_dist + 2)

        self.ax.plot(RRF_x, RRF_y, color=col, ls="--")
        bbox = dict(boxstyle='round', facecolor=col, alpha=alpha)
        if add_text:
            self.ax.text(*text_at, text, color=text_col, bbox=bbox)

    def add_random(self, text_at=None, col='black', add_text=True):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        if text_at is None:
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
            text_at = (
                np.average(xlim) - 0.07 * (xlim[1]-xlim[0]),
                np.average(xlim) + 0.07 * (ylim[1]-ylim[0]),
            )

        bbox = dict(boxstyle='round', facecolor='0.65')
        if add_text:
            self.ax.text(*text_at, "random", color=col, bbox=bbox)
        xlim = [max(x, 0) for x in xlim]
        if self.result_format == "percentage":
            xlim = [min(x, 100) for x in xlim]
        self.ax.plot(xlim, xlim, color='black', ls="--")

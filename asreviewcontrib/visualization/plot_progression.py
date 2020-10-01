import numpy as np

from asreviewcontrib.visualization.plot_base import PlotBase


def _gaussian_window(rel_ids, sigma):
    factors = np.exp(-rel_ids**2 / sigma**2)
    return factors / np.sum(factors)


class PlotProgression(PlotBase):
    def __init__(self,
                 analyses,
                 result_format="percentage",
                 thick=None,
                 sigma=25,
                 window=40):
        """Class for the Regression plot."""
        super(PlotProgression, self).__init__(analyses)
        self.col = {}
        self.result_format = result_format

        if thick is None:
            thick = {key: True for key in list(self.analyses)}
        self.thick = thick

        for i, data_key in enumerate(reversed(self.analyses)):
            analysis = self.analyses[data_key]
            inc_found = analysis.inclusions_found(result_format="number")

            dy_inc = (inc_found[1] - np.append([0], inc_found[1][:-1]))

            self.col[data_key] = "C" + str((len(self.analyses) - 1 - i) % 10)
            col = self.col[data_key]

            if self.thick[data_key]:
                lw = 2
            else:
                lw = 0.7

            smooth_inc_perc = []
            for i in range(len(dy_inc)):
                idx = np.arange(max(0, i - window),
                                min(len(dy_inc), i + window + 1))
                factor = _gaussian_window(idx - i, sigma)
                smooth_inc_perc.append(np.sum(dy_inc[idx] * factor))

            if self.result_format == "percentage":
                x_values = 100 * inc_found[0] / len(analysis.labels)
            else:
                x_values = inc_found[0]
            myplot, = self.ax.plot(x_values,
                                   100 * np.array(smooth_inc_perc),
                                   color=col,
                                   lw=lw)
            if self.thick[data_key]:
                self.legend_plt.append(myplot)
                self.legend_name.append(data_key)

        if self.result_format == "percentage":
            self.ax.set_xlabel("% papers reviewed")
        else:
            self.ax.set_xlabel("# papers reviewed")

        self.ax.set_ylabel("% of proposed papers accepted")

    def set_legend(self, loc="upper right"):
        super(PlotProgression, self).set_legend(loc=loc)

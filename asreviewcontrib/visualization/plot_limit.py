import numpy as np

from asreviewcontrib.visualization.plot_base import PlotBase


class PlotLimit(PlotBase):
    def __init__(self,
                 analyses,
                 prob_allow_miss=[0.1, 0.5, 2.0],
                 result_format="percentage"):
        """Class for the Limit plot."""
        super(PlotLimit, self).__init__(analyses)

        self.legend_plt = []
        self.legend_name = []
        linestyles = ['-', '--', '-.', ':']
        self.result_format = result_format

        for i, data_key in enumerate(self.analyses):
            res = self.analyses[data_key].limits(
                prob_allow_miss=prob_allow_miss, result_format=result_format)
            x_range = res["x_range"]
            col = "C" + str(i % 10)

            for i_limit, limit in enumerate(res["limits"]):
                ls = linestyles[i_limit % len(linestyles)]
                my_plot, = self.ax.plot(x_range,
                                        np.array(limit) + np.array(x_range),
                                        color=col,
                                        ls=ls)
                if i_limit == 0:
                    self.legend_plt.append(my_plot)
                    self.legend_name.append(f"{data_key}")

        self.ax.plot(x_range, x_range, color="black", ls='--')
        if result_format == "percentage":
            self.ax.set_xlabel("% of papers read")
            self.ax.set_ylabel("Estimate of % of papers that need to be read")
        else:
            self.ax.set_xlabel("# of papers read")
            self.ax.set_ylabel("Estimate of # of papers that need to be read")
        self.ax.set_title("Articles left to read")

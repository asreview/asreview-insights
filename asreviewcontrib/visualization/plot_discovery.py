from asreviewcontrib.visualization.plot_base import PlotBase


class PlotDiscovery(PlotBase):
    def __init__(self, analyses, result_format="percentage"):
        """Class for the Discovery plot."""
        super(PlotDiscovery, self).__init__(analyses)
        self.result_format = result_format

        avg_times = []
        for analysis in self.analyses.values():
            results = analysis.avg_time_to_discovery(
                result_format=result_format)
            avg_times.append(list(results.values()))

        if result_format == "number":
            self.ax.hist(avg_times,
                         30,
                         histtype='bar',
                         density=False,
                         label=self.analyses.keys())
            self.ax.set_xlabel("# Reviewed")
            self.ax.set_ylabel("# of papers included")
        else:
            self.ax.hist(avg_times,
                         30,
                         histtype='bar',
                         density=True,
                         label=self.analyses.keys())
            self.ax.set_xlabel("% Reviewed")
            self.ax.set_ylabel("Fraction of papers included")

    def set_legend(self, loc="upper right"):
        self.ax.legend(loc=loc)

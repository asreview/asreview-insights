import matplotlib.pyplot as plt


class PlotBase():
    def __init__(self, analyses):
        """
        Plot the number of queries that turned out to be included
        in the final review.
        """
        super(PlotBase, self).__init__()
        self.legend_name = []
        self.legend_plt = []
        self.fig, self.ax = plt.subplots()
        self.analyses = analyses

    def set_legend(self, loc="lower right"):
        self.ax.legend(self.legend_plt, self.legend_name, loc=loc)

    def set_grid(self):
        self.ax.grid()

    def set_xlim(self, x_start, x_end):
        self.ax.set_xlim(x_start, x_end)

    def set_ylim(self, y_start, y_end):
        self.ax.set_ylim(y_start, y_end)

    def show(self):
        plt.show()

    def save(self, fp, *args, **kwargs):
        self.fig.savefig(fp, *args, **kwargs)

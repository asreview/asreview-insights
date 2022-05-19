import argparse
import json

import matplotlib.pyplot as plt

# from asreview.config import LOGGER_EXTENSIONS
from asreview.entry_points import BaseEntryPoint
from asreview import open_state

from asreviewcontrib.insights import plot_recall
from asreviewcontrib.insights import plot_wss
from asreviewcontrib.insights import plot_erf
from asreviewcontrib.insights.stats import get_stats, print_stats

PLOT_TYPES = ['recall']
TYPE_TO_FUNC = {'recall': plot_recall, 'wss': plot_wss, 'erf': plot_erf}


class PlotEntryPoint(BaseEntryPoint):
    description = "Plotting functionality for ASReview files."
    extension_name = "asreview-insights"

    @property
    def version(self):
        from asreviewcontrib.insights.__init__ import __version__
        return __version__

    def execute(self, argv):
        parser = argparse.ArgumentParser(prog='asreview plot')
        parser.add_argument("plot_type",
                            metavar='type',
                            type=str,
                            default="recall",
                            help="Plot type. Default 'recall'.")
        parser.add_argument('asreview_files',
                            metavar='asreview_files',
                            type=str,
                            nargs='+',
                            help='A (list of) ASReview files.')
        # parser.add_argument('--show_priors',
        #                     metavar='priors',
        #                     type=bool,
        #                     default=False,
        #                     help='Show records used as prior knowledge '
        #                     'in the plot.')
        # parser.add_argument('--x_relative',
        #                     type=bool,
        #                     default=True,
        #                     help='Make use of relative coordinates on'
        #                     ' the x-axis. Default: True.')
        # parser.add_argument('--y_relative',
        #                     type=bool,
        #                     default=True,
        #                     help='Make use of relative coordinates on'
        #                     ' the y-axis. Default: True.')
        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=f"asreview-insights: {self.version}",
        )
        parser.add_argument(
            "-o",
            "--output",
            default=None,
            help='Save the plot to a file. File formats are detected '
            ' by the matplotlib library, check there to see available '
            'formats.')
        args = parser.parse_args(argv)

        if len(args.asreview_files) > 1:
            raise ValueError("Plotting multiple project files"
                             " via the CLI is not supported yet.")

        with open_state(args.asreview_files[0]) as s:

            fig, ax = plt.subplots()
            plot_func = TYPE_TO_FUNC[args.plot_type]
            plot_func(ax,
                      s
                      # priors=args.priors,
                      # x_relative=args.x_relative,
                      # y_relative=args.y_relative
                      )

            if args.output:
                fig.savefig(args.output)
            else:
                plt.show()


class StatsEntryPoint(BaseEntryPoint):
    description = "Statistics and metrics entry point."
    extension_name = "asreview-insights"

    @property
    def version(self):
        from asreviewcontrib.insights.__init__ import __version__
        return __version__

    def execute(self, argv):
        parser = argparse.ArgumentParser(prog='asreview stats')
        parser.add_argument('asreview_files',
                            metavar='asreview_files',
                            type=str,
                            nargs='+',
                            help='A combination of data directories or files.')
        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=f"asreview-insights: {self.version}",
        )
        parser.add_argument(
            '--recall',
            metavar='recall',
            type=float,
            default=[0.1, 0.25, 0.5, 0.75, 0.9],
            nargs='+',
            help='A (list of) values to compute the recall at.')
        parser.add_argument('--wss_recall',
                            metavar='wss',
                            type=float,
                            nargs='+',
                            default=[0.95],
                            help='A (list of) values to compute the wss at.')
        parser.add_argument('--erf',
                            metavar='erf',
                            type=float,
                            nargs='+',
                            default=[0.95],
                            help='A (list of) values to compute the erf at.')
        parser.add_argument('--show_priors',
                            metavar='priors',
                            type=bool,
                            default=False,
                            help='Show records used as prior knowledge '
                            'in the plot.')
        parser.add_argument('--x_relative',
                            type=bool,
                            default=True,
                            help='Make use of relative coordinates on'
                            ' the x-axis. Default: True.')
        parser.add_argument('--y_relative',
                            type=bool,
                            default=True,
                            help='Make use of relative coordinates on'
                            ' the y-axis. Default: True.')
        parser.add_argument(
            "-o",
            "--output",
            default=None,
            help='Save the statistics and metrics to a JSON file.')
        args = parser.parse_args(argv)

        if len(args.asreview_files) > 1:
            raise ValueError("Computing metrics for multiple project files"
                             " via the CLI is not supported yet.")

        with open_state(args.asreview_files[0]) as s:
            stats = get_stats(s,
                              recall=args.recall,
                              wss=args.wss,
                              erf=args.erf,
                              priors=args.priors,
                              x_relative=args.x_relative,
                              y_relative=args.y_relative)
            print_stats(stats)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(stats, f, indent=4)

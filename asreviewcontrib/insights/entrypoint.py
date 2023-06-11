import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
from asreview import open_state
from asreview.entry_points import BaseEntryPoint

from asreviewcontrib.insights import plot_erf
from asreviewcontrib.insights import plot_recall
from asreviewcontrib.insights import plot_wss
from asreviewcontrib.insights.metrics import get_metrics
from asreviewcontrib.insights.metrics import print_metrics
from asreviewcontrib.insights.utils import _iter_states

TYPE_TO_FUNC = {"recall": plot_recall, "wss": plot_wss, "erf": plot_erf}


class PlotEntryPoint(BaseEntryPoint):
    description = "Plotting functionality for ASReview files."
    extension_name = "asreview-insights"

    @property
    def version(self):
        from asreviewcontrib.insights.__init__ import __version__

        return __version__

    def execute(self, argv):
        parser = argparse.ArgumentParser(prog="asreview plot")
        parser.add_argument(
            "plot_type",
            metavar="type",
            type=str,
            default="recall",
            help="Plot type. Default 'recall'.",
        )
        parser.add_argument(
            "asreview_files",
            metavar="asreview_files",
            type=str,
            nargs="+",
            help="A (list of) ASReview files.",
        )
        parser.add_argument(
            "--priors",
            action="store_true",
            help="Include records used as prior knowledge " "in the plot.",
        )
        parser.add_argument(
            "--no-priors",
            dest="priors",
            action="store_false",
            help="Exclude records used as prior knowledge " "in the plot. Default.",
        )
        parser.set_defaults(priors=False)
        parser.add_argument(
            "--x_absolute",
            action="store_true",
            help="Make use of absolute coordinates on" " the x-axis.",
        )
        parser.add_argument(
            "--y_absolute",
            action="store_true",
            help="Make use of absolute coordinates on" " the y-axis.",
        )
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
            help="Save the plot to a file. File formats are detected "
            " by the matplotlib library, check there to see available "
            "formats.",
        )
        args = parser.parse_args(argv)

        fig, ax = plt.subplots()
        plot_func = TYPE_TO_FUNC[args.plot_type]
        show_legend = False if len(args.asreview_files) == 1 else True
        state_obj = _iter_states(args.asreview_files)
        legend_values = [Path(fp).stem for fp in args.asreview_files]

        plot_func(
            ax,
            state_obj,
            priors=args.priors,
            x_absolute=args.x_absolute,
            y_absolute=args.y_absolute,
            show_legend=show_legend,
            legend_values=legend_values,
        )

        if args.output:
            fig.savefig(args.output)
        else:
            plt.show()


class MetricsEntryPoint(BaseEntryPoint):
    description = "Metrics entry point."
    extension_name = "asreview-insights"

    @property
    def version(self):
        from asreviewcontrib.insights.__init__ import __version__

        return __version__

    def execute(self, argv):
        parser = argparse.ArgumentParser(prog="asreview metrics")
        parser.add_argument(
            "asreview_files",
            metavar="asreview_files",
            type=str,
            nargs="+",
            help="A (list of) ASReview files.",
        )
        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=f"asreview-insights: {self.version}",
        )
        parser.add_argument(
            "--recall",
            metavar="recall",
            type=float,
            default=[0.1, 0.25, 0.5, 0.75, 0.9],
            nargs="+",
            help="A (list of) values to compute the recall at.",
        )
        parser.add_argument(
            "--wss",
            metavar="wss",
            type=float,
            nargs="+",
            default=[0.95],
            help="A (list of) values to compute the wss at.",
        )
        parser.add_argument(
            "--erf",
            metavar="erf",
            type=float,
            nargs="+",
            default=[0.10],
            help="A (list of) values to compute the erf at.",
        )
        parser.add_argument(
            "--cm",
            metavar="cm",
            type=float,
            nargs="+",
            default=[0.1, 0.25, 0.5, 0.75, 0.8, 0.85, 0.9, 0.95, 1],
            help="A (list of) values to compute the cm at.",
        )
        parser.add_argument(
            "--priors",
            action="store_true",
            help="Include records used as prior knowledge " "in the metrics.",
        )
        parser.add_argument(
            "--no-priors",
            dest="priors",
            action="store_false",
            help="Exclude records used as prior knowledge " "in the metrics. Default.",
        )
        parser.set_defaults(priors=False)
        parser.add_argument(
            "--x_absolute",
            action="store_true",
            help="Make use of absolute coordinates on" " the x-axis.",
        )
        parser.add_argument(
            "--y_absolute",
            action="store_true",
            help="Make use of absolute coordinates on" " the y-axis.",
        )
        parser.add_argument(
            "-o",
            "--output",
            default=None,
            help="Save the metrics and results to a JSON file.",
        )
        args = parser.parse_args(argv)

        output_dict = {}
        for asreview_file in args.asreview_files:
            with open_state(asreview_file) as s:
                if len(args.asreview_files) > 1:
                    print(f"Calculating metrics for {asreview_file}")
                stats = get_metrics(
                    s,
                    recall=args.recall,
                    wss=args.wss,
                    erf=args.erf,
                    cm=args.cm,
                    priors=args.priors,
                    x_absolute=args.x_absolute,
                    y_absolute=args.y_absolute,
                    version=self.version,
                )
                output_dict[asreview_file] = stats
                print_metrics(stats)

        if args.output:
            if len(args.asreview_files) == 1:
                output_dict = output_dict[args.asreview_files[0]]
            with open(args.output, "w") as f:
                json.dump(output_dict, f, indent=4)

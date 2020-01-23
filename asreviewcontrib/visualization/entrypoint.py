#!/usr/bin/env python

import sys
from asreviewcontrib.visualization import Plot
from asreview.entry_points import BaseEntryPoint


class PlotEntryPoint(BaseEntryPoint):
    description = "Plotting functionality for logging files produced by "\
        "ASReview."

    def execute(self, argv):
        main(argv)


def main(argv=sys.argv[1:]):
    if len(argv) > 0:
        json_dirs = argv
    else:
        json_dirs = ["output"]

    with Plot.from_dirs(json_dirs) as plot:
        plot.plot_time_to_inclusion("../hyperopt/data/depression.json")
        plot.plot_inc_found(result_format="percentage")
        plot.plot_time_to_discovery()
        plot.plot_limits()

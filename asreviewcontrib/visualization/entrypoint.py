#!/usr/bin/env python

import argparse

from asreview.entry_points import BaseEntryPoint

from asreviewcontrib.visualization import Plot
import logging

PLOT_TYPES = ['inclusions', 'discovery', 'limits']


class PlotEntryPoint(BaseEntryPoint):
    description = "Plotting functionality for logging files produced by "\
        "ASReview."

    def execute(self, argv):
        parser = _parse_arguments()
        args_dict = vars(parser.parse_args(argv))

        if args_dict['type'] == 'all':
            types = PLOT_TYPES
        else:
            arg_types = args_dict['type'].split(',')
            types = []
            for plot_type in arg_types:
                if plot_type not in PLOT_TYPES:
                    logging.warning(f'Plotting type "{plot_type} unknown."')
                else:
                    types.append(plot_type)

        if args_dict["absolute_format"]:
            result_format = "number"
        else:
            result_format = "percentage"

        with Plot.from_dirs(args_dict["data_dirs"]) as plot:
            if "inclusions" in types:
                plot.plot_inc_found(result_format=result_format)
            if "discovery" in types:
                plot.plot_time_to_discovery(result_format=result_format)
            if "limits" in types:
                plot.plot_limits(result_format=result_format)


def _parse_arguments():
    parser = argparse.ArgumentParser(prog='asreview plot')
    parser.add_argument(
        'data_dirs',
        metavar='N',
        type=str,
        nargs='+',
        help='Data directories.'
    )
    parser.add_argument(
        "-t", "--type",
        type=str,
        default="all",
        help="Type of plot to make. Separate by commas (no spaces) for"
        " multiple plots."
    )
    parser.add_argument(
        "-a", "--absolute-values",
        dest="absolute_format",
        action='store_true',
        help='Use absolute values on the axis instead of percentages.'
    )
    return parser

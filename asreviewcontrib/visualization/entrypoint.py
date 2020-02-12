# Copyright 2020 The ASReview Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

from asreview.config import LOGGER_EXTENSIONS
from asreview.entry_points import BaseEntryPoint

from asreviewcontrib.visualization import Plot
import logging

PLOT_TYPES = ['inclusions', 'discovery', 'limits']


class PlotEntryPoint(BaseEntryPoint):
    description = "Plotting functionality for logging files produced by "\
        "ASReview."
    extension_name = "asreview-visualization"

    def __init__(self):
        from asreviewcontrib.visualization.__init__ import __version__
        super(PlotEntryPoint, self).__init__()

        self.version = __version__

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

        prefix = args_dict["prefix"]
        legend = not args_dict["no_legend"]
        with Plot.from_dirs(args_dict["data_dirs"], prefix=prefix) as plot:
            if len(plot.analyses) == 0:
                print(f"No log files found in {args_dict['data_dirs']}.\n"
                      f"To be detected log files have to start with '{prefix}'"
                      f" and end with one of the following: \n"
                      f"{', '.join(LOGGER_EXTENSIONS)}.")
                return
            if "inclusions" in types:
                plot.plot_inc_found(result_format=result_format, legend=legend,
                                    abstract_only=args_dict["abstract_only"],
                                    wss_value=args_dict["wss_value"])
            if "discovery" in types:
                plot.plot_time_to_discovery(result_format=result_format)
            if "limits" in types:
                plot.plot_limits(result_format=result_format)


def _parse_arguments():
    parser = argparse.ArgumentParser(prog='asreview plot')
    parser.add_argument(
        'data_dirs',
        metavar='DATA_FP',
        type=str,
        nargs='+',
        help='A combination of data directories or files.'
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
    parser.add_argument(
        "--prefix",
        default="",
        help='Filter files in the data directory to only contain files'
             'starting with a prefix.'
    )
    parser.add_argument(
        "--abstract_only",
        default=False,
        action="store_true",
        help="Use after abstract screening as the inclusions/exclusions."
    )
    parser.add_argument(
        "--no_legend",
        default=False,
        action="store_true",
        help="Don't show a legend with the plot."
    )
    parser.add_argument(
        "--wss_value",
        default=False,
        action="store_true",
        help="Add WSS values to plot."
    )
    return parser

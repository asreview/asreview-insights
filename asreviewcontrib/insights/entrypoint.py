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
import json
import logging

import matplotlib.pyplot as plt

# from asreview.config import LOGGER_EXTENSIONS
from asreview.entry_points import BaseEntryPoint
from asreview import open_state

# from asreviewcontrib.visualization import Plot
# from asreviewcontrib.visualization.quick import progression_plot
# from asreviewcontrib.visualization.quick import limit_plot
# from asreviewcontrib.visualization.quick import discovery_plot
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
        parser.add_argument("type",
                            type=str,
                            default="recall",
                            help="Plot type. Default 'recall'.")
        parser.add_argument('asreview_files',
                            metavar='asreview_files',
                            type=str,
                            nargs='+',
                            help='A (list of) ASReview files.')
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

        with open_state(args.asreview_files[0]) as s:

            fig, ax = plt.subplots()
            plot_func = TYPE_TO_FUNC[args.type]
            plot_func(ax, s)

            if args.output:
                fig.savefig(args.output)


class StatsEntryPoint(BaseEntryPoint):
    description = "Statistics and metrics entry point."
    extension_name = "asreview-insights"

    @property
    def version(self):
        from asreviewcontrib.insights.__init__ import __version__
        return __version__

    def execute(self, argv):
        parser = argparse.ArgumentParser(prog='asreview plot')
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
            "-o",
            "--output",
            default=None,
            help='Save the statistics and metrics to a JSON file.')
        args = parser.parse_args(argv)

        with open_state(args.asreview_files[0]) as s:
            stats = get_stats()
            print_stats(stats)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(stats, f, indent=4)

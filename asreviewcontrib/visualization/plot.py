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

from collections import OrderedDict
import os

import matplotlib.pyplot as plt
import numpy as np

from asreview.analysis.analysis import Analysis
from asreviewcontrib.visualization.plot_inclusions import PlotInclusions


class Plot():
    def __init__(self, paths, prefix="result"):
        self.analyses = OrderedDict()
        self.is_file = OrderedDict()

        for path in paths:
            new_analysis = Analysis.from_path(path, prefix=prefix)
            if new_analysis is not None:

                data_key = new_analysis.key
                self.analyses[data_key] = new_analysis
                if os.path.isfile(path):
                    self.is_file[data_key] = True
                else:
                    self.is_file[data_key] = False

    def __enter__(self):
        return self

    def __exit__(self, *_, **__):
        for analysis in self.analyses.values():
            analysis.close()

    @classmethod
    def from_paths(cls, paths, prefix="result"):
        plot_inst = Plot(paths, prefix=prefix)
        return plot_inst

    def new(self, plot_type="inclusions", **kwargs):
        if plot_type == "inclusions":
            thick = kwargs.pop("thick", None)
            if thick is None:
                thick = {key: not f for key, f in self.is_file.items()}
            return PlotInclusions(self.analyses, thick=thick, **kwargs)
        raise ValueError(f"Error: plot type '{plot_type}' not found.")

    def plot_time_to_inclusion(self, X_fp):
        for data_key, analysis in self.analyses.items():
            results = analysis.time_to_inclusion(X_fp)
            for key in results["ttd"]:
                plt.plot(results["x_range"], results["ttd"][key],
                         label=data_key + " - " + key)
        plt.legend()
        plt.show()

    def plot_time_to_discovery(self, result_format="percentage"):
        avg_times = []
        for analysis in self.analyses.values():
            results = analysis.avg_time_to_discovery(
                result_format=result_format)
            avg_times.append(list(results.values()))

        if result_format == "number":
            plt.hist(avg_times, 30, histtype='bar', density=False,
                     label=self.analyses.keys())
            plt.xlabel("# Reviewed")
            plt.ylabel("# of papers included")
        else:
            plt.hist(avg_times, 30, histtype='bar', density=True,
                     label=self.analyses.keys())
            plt.xlabel("% Reviewed")
            plt.ylabel("Fraction of papers included")
        plt.legend()
        plt.show()

    def plot_inc_progression(self, sigma=30, window=50):
        legend_name = []
        legend_plt = []

        def gaussian_window(rel_ids, sigma):
            factors = np.exp(-rel_ids**2/sigma**2)
            return factors/np.sum(factors)

        for i, data_key in enumerate(self.analyses):
            analysis = self.analyses[data_key]
            inc_found = analysis.inclusions_found(result_format="number")

            dy_inc = (inc_found[1] - np.append([0], inc_found[1][:-1]))

            col = "C"+str(i % 10)

            legend_name.append(data_key)
            smooth_inc_perc = []
            for i in range(len(dy_inc)):
                idx = np.arange(max(0, i-window), min(len(dy_inc), i+window+1))
                factor = gaussian_window(idx - i, sigma)
                smooth_inc_perc.append(np.sum(dy_inc[idx]*factor))

            myplot, = plt.plot(inc_found[0], 100*np.array(smooth_inc_perc), color=col)
            legend_plt.append(myplot)

        plt.legend(legend_plt, legend_name, loc="upper right")

        plt.xlabel("# papers reviewed")
        plt.ylabel("% of proposed papers accepted")
        plt.grid()
        plt.show()

    def plot_limits(self, prob_allow_miss=[0.1, 0.5, 2.0],
                    result_format="percentage"):
        legend_plt = []
        legend_name = []
        linestyles = ['-', '--', '-.', ':']

        for i, data_key in enumerate(self.analyses):
            res = self.analyses[data_key].limits(
                prob_allow_miss=prob_allow_miss,
                result_format=result_format)
            x_range = res["x_range"]
            col = "C"+str(i % 10)

            for i_limit, limit in enumerate(res["limits"]):
                ls = linestyles[i_limit % len(linestyles)]
                my_plot, = plt.plot(x_range, np.array(limit)+np.array(x_range),
                                    color=col, ls=ls)
                if i_limit == 0:
                    legend_plt.append(my_plot)
                    legend_name.append(f"{data_key}")

        plt.plot(x_range, x_range, color="black", ls='--')
        if result_format == "percentage":
            plt.xlabel("% of papers read")
            plt.ylabel("Estimate of % of papers that need to be read")
        else:
            plt.xlabel("# of papers read")
            plt.ylabel("Estimate of # of papers that need to be read")
        plt.legend(legend_plt, legend_name, loc="upper right")
        plt.title("Articles left to read")
        plt.grid()
        plt.show()

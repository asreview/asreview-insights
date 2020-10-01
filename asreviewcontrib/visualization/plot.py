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

import os
from collections import OrderedDict

from asreview.analysis import Analysis

from asreviewcontrib.visualization.plot_discovery import PlotDiscovery
from asreviewcontrib.visualization.plot_inclusions import PlotInclusions
from asreviewcontrib.visualization.plot_limit import PlotLimit
from asreviewcontrib.visualization.plot_progression import PlotProgression


class Plot():
    def __init__(self, paths, prefix="result"):
        self.analyses = OrderedDict()
        self.is_file = OrderedDict()

        if isinstance(paths, dict):
            for path, key in paths.items():
                new_analyis = Analysis.from_path(path, prefix=prefix)
                if new_analyis is None:
                    continue
                if key is None:
                    key = new_analyis.key
                else:
                    new_analyis.key = key
                self.analyses[key] = new_analyis
                if os.path.isfile(path):
                    self.is_file[key] = True
                else:
                    self.is_file[key] = False
        else:
            for path in paths:
                new_analysis = Analysis.from_path(path, prefix=prefix)
                if new_analysis is None:
                    continue
                data_key = new_analysis.key
                self.analyses[data_key] = new_analysis
                if os.path.isfile(path):
                    self.is_file[data_key] = True
                else:
                    self.is_file[data_key] = False
        all_files = all(self.is_file.values())
        if all_files:
            self.thick = {key: True for key in list(self.analyses)}
        else:
            self.thick = {key: not f for key, f in self.is_file.items()}

    def __enter__(self):
        return self

    def __exit__(self, *_, **__):
        for analysis in self.analyses.values():
            analysis.close()

    @classmethod
    def from_paths(cls, paths, prefix="result"):
        plot_inst = Plot(paths, prefix=prefix)
        return plot_inst

    def new(self, plot_type="inclusion", **kwargs):
        thick = kwargs.pop("thick", None)
        if thick is None:
            thick = self.thick
        if plot_type == "inclusion":
            return PlotInclusions(self.analyses, thick=thick, **kwargs)
        elif plot_type == "progression":
            return PlotProgression(self.analyses, thick=thick, **kwargs)
        elif plot_type == "discovery":
            return PlotDiscovery(self.analyses, **kwargs)
        elif plot_type == "limit":
            return PlotLimit(self.analyses, **kwargs)
        raise ValueError(f"Error: plot type '{plot_type}' not found.")

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


def inclusion_plot(plot, output=None, show_metric_labels=True, **kwargs):
    """Make an inclusion plot."""
    all_files = all(plot.is_file.values())

    inc_plot = plot.new("inclusion", **kwargs)
    inc_plot.set_grid()

    for key in list(plot.analyses):
        if all_files or not plot.is_file[key]:
            inc_plot.add_wss(
                key, 95, add_text=show_metric_labels, add_value=True)
            inc_plot.add_rrf(
                key, 10, add_text=show_metric_labels, add_value=True)
    inc_plot.add_random(add_text=False)

    # TODO {Make legend in flexible argument}
    # inc_plot.set_legend()

    if output is None:
        inc_plot.show()
    else:
        inc_plot.save(output)
        inc_plot.close()


def progression_plot(plot, output=None, **kwargs):
    """Make a progression plot."""
    prog_plot = plot.new("progression", **kwargs)
    prog_plot.set_grid()
    prog_plot.set_legend()
    if output is None:
        prog_plot.show()
    else:
        prog_plot.save(output)
        prog_plot.close()


def discovery_plot(plot, output=None, **kwargs):
    """Make a discovery plot."""
    disc_plot = plot.new("discovery", **kwargs)
    disc_plot.set_legend()
    if output is None:
        disc_plot.show()
    else:
        disc_plot.save(output)
        disc_plot.close()


def limit_plot(plot, output=None, **kwargs):
    """Make a limit plot."""
    limit_plot = plot.new("limit", **kwargs)
    limit_plot.set_legend()
    limit_plot.set_grid()
    if output is None:
        limit_plot.show()
    else:
        limit_plot.save(output)
        limit_plot.close()

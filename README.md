# ASReview Insights

[![PyPI version](https://badge.fury.io/py/asreview-insights.svg)](https://badge.fury.io/py/asreview-insights) [![Downloads](https://pepy.tech/badge/asreview-insights)](https://pepy.tech/project/asreview-insights) ![PyPI - License](https://img.shields.io/pypi/l/asreview-insights) ![Deploy and release](https://github.com/asreview/asreview-insights/workflows/Deploy%20and%20release/badge.svg) ![Build status](https://github.com/asreview/asreview-insights/workflows/test-suite/badge.svg) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6626069.svg)](https://doi.org/10.5281/zenodo.6626069)


This official extension to [ASReview
LAB](https://github.com/asreview/asreview) extends the software with tools for
[plotting](#plot-types) and extracting the [statistical results](#metrics) of
several [performance metrics](#performance-metrics). The extension is
especially useful in combination with the [simulation
functionality](https://asreview.readthedocs.io/en/latest/simulation_overview.html)
of ASReview LAB.


❣️ ASReview Insights is the successor to
[ASReview-visualization](https://pypi.org/project/asreview-visualization/).
ASReview insights is available for [ASReview
LAB](https://github.com/asreview/asreview/discussions/975) version 1 or later.
Use ASReview visualization for versions 0.x.

## Installation

ASReview Insights can be installed from PyPI:

``` bash
pip install asreview-insights
```

After installation, check if the `asreview-insights` package is listed as an
extension. Use the following command:

```bash
asreview --help
```

It should list the 'plot' subcommand and the 'metrics' subcommand.

## Performance metrics

The ASReview Insights extension is useful for measuring the performance of
active learning models on collections of binary labeled text. The extension
can be used after performing a simulation study that involves mimicking the
screening process with a specific model. As it is already known which records
are labeled relevant, the simulation can automatically reenact the screening
process as if a screener were using active learning. The performance of one or
multiple models can be measured by different metrics and the
ASReview Insights extension can plot or compute the values for such metrics
from ASReview project files.

The recall is the proportion of relevant records that have been found at a
certain point during the screening phase. It is sometimes also called the
proportion of Relevant Record Found (RRF) after screening an X% of the total
records. For example, the RRF@10 is the recall (i.e., the proportion of the
total number of relevant records) at screening 10% of the total number of
records available in the dataset.

A variation is the Extra Relevant records Found (ERF), which is the proportion
of relevant records found after correcting for the number of relevant records
found via random screening (assuming a uniform distribution of relevant
records).

The Work Saved over Sampling (WSS) is a measure of "the work saved over and
above the work saved by simple sampling for a given level of recall" ([Cohen
et al., 2006]((https://doi.org/10.1197/jamia.m1929)). It is defined as the
proportion of records a screener does **not** have to screen compared to
random reading after providing the prior knowledge used to train the first
iteration of the model. The WSS is typically measured at a recall of .95
(WSS@95), reflecting the proportion of records saved by using active learning
at the cost of failing to identify .05 of relevant publications.

The following plot illustrates the differences between the metrics Recall
(y-axis), WSS (blue line), and ERF (red line). The dataset contains 1.000
hypothetical records with labels. The stepped line on the diagonal is the
naive labeling approach (screening randomly sorted records).

![ASReview metrics explained](https://github.com/asreview/asreview-insights/blob/master/docs/stats_explainer.png)


## Basic usage

The ASReview Insights package extends ASReview LAB with two new subcommands
(see `asreview --help`): [`plot`](#plot) and [`metrics`](#metrics). The plots
and metrics are derived from an ASReview project file. The ASReview file
(extension `.asreview`) can be
[exported](https://asreview.readthedocs.io/en/latest/manage.html#export-project)
from ASReview LAB after a
[simulation](https://asreview.readthedocs.io/en/latest/simulation_overview.html),
or it is generated from running a [simulation via the command
line](https://asreview.readthedocs.io/en/latest/simulation_cli.html).

For example, an ASReview can be generated with:


```python
asreview simulate benchmark:van_de_schoot_2017 -s sim_van_de_schoot_2017.asreview --init_seed 535
```

To use the most basic options of the ASReview Insights extension, run

```bash
asreview plot recall YOUR_ASREVIEW_FILE.asreview
```
where `recall` is the type of the plot, or

```bash
asreview metrics sim_van_de_schoot_2017.asreview
```

More options are described in the sections below. All options can be
obtained via `asreview plot --help` or `asreview metrics --help`.

## `Plot`

### Plot types

#### `recall`

The recall is an important metric to study the performance of active learning
algorithms in the context of information retrieval. ASReview Insights
offers a straightforward command line interface to plot a "recall curve". The
recall curve is the recall at any moment in the active learning process.

To plot the recall curve, you need a ASReview file (extension `.asreview`).To
plot the recall, use this syntax (Replace `YOUR_ASREVIEW_FILE.asreview` by
your ASReview file name.):

```bash
asreview plot recall YOUR_ASREVIEW_FILE.asreview
```

The following plot is the result of simulating the [`van_de_schoot_2017`](https://github.com/asreview/systematic-review-datasets/tree/master/datasets/van_de_Schoot_2017) in
the benchmark platform (command `asreview simulate
benchmark:van_de_schoot_2017 -s sim_van_de_schoot_2017.asreview`).

![Recall plot of Van de Schoot 2017](https://github.com/asreview/asreview-insights/blob/master/figures/tests_recall_sim_van_de_schoot_2017_1.png)

On the vertical axis, you find the recall (i.e, the proportion of the relevant
records) after every labeling decision. The horizontal axis shows the
proportion of  total number of records in the dataset. The steeper the recall
curve, the higher the performance of active learning when comparted to random
screening. The recall curve can also be used to estimate stopping criteria, see
the discussions in [#557](https://github.com/asreview/asreview/discussions/557) and [#1115](https://github.com/asreview/asreview/discussions/1115).


```bash
asreview plot recall YOUR_ASREVIEW_FILE.asreview
```

#### `wss`

The Work Saved over Sampling (WSS) metric is an useful metric to study the
performance of active learning alorithms compared with a naive (random order)
approach at a given level of recall. ASReview Insights offers a
straightforward command line interface to plot the WSS at any level of recall.

To plot the WSS curve, you need a ASReview file (extension `.asreview`). To
plot the WSS, use this syntax (Replace `YOUR_ASREVIEW_FILE.asreview` by your
ASReview file name.):

```bash
asreview plot wss YOUR_ASREVIEW_FILE.asreview
```

The following plot is the result of simulating the [`van_de_schoot_2017`](https://github.com/asreview/systematic-review-datasets/tree/master/datasets/van_de_Schoot_2017) in
the benchmark platform (command `asreview simulate
benchmark:van_de_schoot_2017 -s sim_van_de_schoot_2017.asreview`).

![Recall plot of Van de Schoot 2017](https://github.com/asreview/asreview-insights/blob/master/figures/tests_wss_default_sim_van_de_schoot_2017_1.png)

On the vertical axis, you find the WSS after every labeling decision. The
recall is displayed on the horizontal axis. As shown in the figure, the
WSS is linearly related to the recall.


#### `erf`

The Extra Relevant Records found is a derivative of the recall and presents
the proportion of relevant records found after correcting for the number of
relevant records found via random screening (assuming a uniform distribution
of relevant records).

To plot the WSS curve, you need a ASReview file (extension `.asreview`). To
plot the WSS, use this syntax (Replace `YOUR_ASREVIEW_FILE.asreview` by your
ASReview file name.):


```bash
asreview plot erf YOUR_ASREVIEW_FILE.asreview
```

The following plot is the result of simulating the [`van_de_schoot_2017`](https://github.com/asreview/systematic-review-datasets/tree/master/datasets/van_de_Schoot_2017) in
the benchmark platform (command `asreview simulate
benchmark:van_de_schoot_2017 -s sim_van_de_schoot_2017.asreview`).

![Recall plot of Van de Schoot 2017](https://github.com/asreview/asreview-insights/blob/master/figures/tests_erf_default_sim_van_de_schoot_2017_1.png)

On the vertical axis, you find the ERF after every labeling decision. The
horizontal axis shows the proportion of  total number of records in the
dataset. The steep increase of the ERF in the beginning of the process is
related to the steep recall curve.

### Plotting CLI

Optional arguments for the command line are `--priors` to include prior
knowledge, `--x_absolute` and `--x_absolute` to use absolute axes.

See `asreview plot -h` for all command line arguments.


### Plotting API

To make use of the more advanced features, you can make use of the Python API.
The advantage is that you can tweak every single element of the plot in the
way you like. The following examples show how the Python API can be used. They
make use of matplotlib extensively. See the [Introduction to
Matplotlib](https://matplotlib.org/stable/tutorials/introductory/usage.html)
for examples on using the API.

The following example show how to plot the recall with the API and save the
result. The plot is saved using the matplotlib API.

```python
import matplotlib.pyplot as plt

from asreview import open_state
from asreviewcontrib.insights.plot import plot_recall

with open_state("example.asreview") as s:

    fig, ax = plt.subplots()

    plot_recall(ax, s)

    fig.savefig("example.png")
```

Other options are `plot_wss` and `plot_erf`.

#### Example: Customize plot

It's straightforward to customize the plots if you are familiar with
`matplotlib`. The following example shows how to update the title of the plot.

```python
import matplotlib.pyplot as plt

from asreview import open_state
from asreviewcontrib.insights.plot import plot_wss

with open_state("example.asreview") as s:

    fig, ax = plt.subplots()
    plot_wss(ax, s)

    plt.title("WSS with custom title")

    fig.savefig("example_custom_title.png")
```

![WSS with custom title](https://github.com/asreview/asreview-insights/blob/master/docs/example_custom_title.png)

#### Example: Prior knowledge

It's possible to include prior knowledge to your plot. By default, prior
knowledge is excluded from the plot.

```python
import matplotlib.pyplot as plt

from asreview import open_state
from asreviewcontrib.insights.plot import plot_wss

with open_state("example.asreview") as s:

    fig, ax = plt.subplots()
    plot_wss(ax, s, priors=True)

```

#### Example: Relative versus absolute axes

By default, all axes in ASReview Insights are relative. The API can be used to
change this behavior. The arguments are identical for each plot function.

```python
import matplotlib.pyplot as plt

from asreview import open_state
from asreviewcontrib.insights.plot import plot_wss

with open_state("example.asreview") as s:

    fig, ax = plt.subplots()
    plot_wss(ax, s, x_absolute=True, y_absolute=True)

    fig.savefig("example_absolute_axis.png")
```

![Recall with absolute axes](https://github.com/asreview/asreview-insights/blob/master/docs/example_absolute_axes.png)


#### Example: Multiple curves in one plot

It is possible to have multiple curves in one plot by using the API,
and add a legend.

```python
import matplotlib.pyplot as plt

from asreview import open_state
from asreviewcontrib.insights.plot import plot_recall


fig, ax = plt.subplots()

with open_state("tests/asreview_files/sim_van_de_schoot_2017_1.asreview") as s1:
    plot_recall(ax, s1)

with open_state("tests/asreview_files/"
                "sim_van_de_schoot_2017_logistic.asreview") as s2:
    plot_recall(ax, s2)

ax.lines[0].set_label("Naive Bayes")
ax.lines[2].set_label("Logistic")
ax.legend()

fig.savefig("docs/example_multiple_lines.png")
```
![Recall with multiple lines](https://github.com/asreview/asreview-insights/blob/master/docs/example_multiple_lines.png)

## `metrics`

The `metrics` subcommand in ASReview Insights can be used to compute metrics
at given values. The easiest way to get compute metrics for a ASReview project
file is with the following command don the command line:

```
asreview metrics sim_van_de_schoot_2017.asreview
```

which results in

```
    "asreviewVersion": "1.0",
    "apiVersion": "1.0",
    "data": {
        "items": [
            {
                "id": "recall",
                "title": "Recall",
                "value": [
                    [
                        0.1,
                        1.0
                    ],
                    [
                        0.25,
                        1.0
                    ],
                    [
                        0.5,
                        1.0
                    ],
                    [
                        0.75,
                        1.0
                    ],
                    [
                        0.9,
                        1.0
                    ]
                ]
            },
            {
                "id": "wss",
                "title": "Work Saved over Sampling",
                "value": [
                    [
                        0.95,
                        0.8913851624373686
                    ]
                ]
            },
            {
                "id": "erf",
                "title": "Extra Relevant record Found",
                "value": [
                    [
                        0.1,
                        0.9047619047619048
                    ]
                ]
            }
        ]
    }
}
```

Each available item has two values. The first value is the value at which the
metric is computed. In the plots above, this is the x-axis. The second value
is the results of the metric. Some metrics are computed for multiple values.

| Metric | Description pos. 1 | Description pos. 2 | Default |
|---|---|---|---|
| `recall` | Labels | Recall | 0.1, 0.25, 0.5, 0.75, 0.9 |
| `wss` | Recall | Work Saved over Sampling at recall | 0.95 |
| `erf` | Labels | ERF | 0.10 |


### Override default values

It is possible to override the default values of `asreview metrics`. See
`asreview metrics -h` for more information or see the example below.

```
asreview metrics sim_van_de_schoot_2017.asreview --wss 0.9 0.95
```

```
{
    "asreviewVersion": "1.0",
    "apiVersion": "1.0",
    "data": {
        "items": [
            {
                "id": "recall",
                "title": "Recall",
                "value": [
                    [
                        0.1,
                        1.0
                    ],
                    [
                        0.25,
                        1.0
                    ],
                    [
                        0.5,
                        1.0
                    ],
                    [
                        0.75,
                        1.0
                    ],
                    [
                        0.9,
                        1.0
                    ]
                ]
            },
            {
                "id": "wss",
                "title": "Work Saved over Sampling",
                "value": [
                    [
                        0.9,
                        0.8474220139001132
                    ],
                    [
                        0.95,
                        0.8913851624373686
                    ]
                ]
            },
            {
                "id": "erf",
                "title": "Extra Relevant record Found",
                "value": [
                    [
                        0.1,
                        0.9047619047619048
                    ]
                ]
            }
        ]
    }
}
```

### Save metrics to file

Metrics can be saved to a file in the JSON format. Use the flag `-o` or
`--output`.

```
asreview metrics sim_van_de_schoot_2017.asreview -o my_file.json
```

### Metrics CLI

Optional arguments for the command line are `--priors` to include prior
knowledge, `--x_absolute` and `--x_absolute` to use absolute axes.

See `asreview metrics -h` for all command line arguments.

### Metrics API

Metrics are easily accesible with the ASReview Insights API.

Compute the recall after reading half of the dataset.

```python

from asreview import open_state
from asreviewcontrib.insights.metrics import recall

with open_state("example.asreview") as s:

    print(recall(s, 0.5))
```

Other metrics are available like `wss` and `erf`.

#### Example: Prior knowledge

It's possible to include prior knowledge to your metric. By default, prior
knowledge is excluded from the metric.

```python

from asreview import open_state
from asreviewcontrib.insights.metrics import recall

with open_state("example.asreview") as s:

    print(recall(s, 0.5, priors=True))
```

## License

This extension is published under the [MIT license](/LICENSE).

## Contact

This extension is part of the ASReview project ([asreview.ai](https://asreview.ai)). It is maintained by the
maintainers of ASReview LAB. See [ASReview
LAB](https://github.com/asreview/asreview) for contact information and more
resources.

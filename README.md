# asreview-insights

## This package is currently under development. See [ASReview-visualization](https://pypi.org/project/asreview-visualization/) for stable version compatible with ASReview LAB <=0.19.x.

[![PyPI version](https://badge.fury.io/py/asreview-insights.svg)](https://badge.fury.io/py/asreview-insights) [![Downloads](https://pepy.tech/badge/asreview-insights)](https://pepy.tech/project/asreview-insights) ![PyPI - License](https://img.shields.io/pypi/l/asreview-insights) ![Deploy and release](https://github.com/asreview/asreview-insights/workflows/Deploy%20and%20release/badge.svg) ![Build status](https://github.com/asreview/asreview-insights/workflows/test-suite/badge.svg)

❣️ ASReview-insights is the successor to [ASReview-visualization](https://pypi.org/project/asreview-visualization/). ASReview insights is available for version 1 or later. Use ASReview visualization for versions 0.x.

This official extension to [ASReview
LAB](https://github.com/asreview/asreview) extends asreview with tools for
plotting and extraction of metrics and statistics. The extension is especially
useful in combination with the simulation feature of ASReview LAB.


## Installation

ASReview-insights can be installed from PyPI:

``` bash
pip install --dev asreview-insights
```

After installation, check if the ` asreview-insights` package is listed as an
extension. Use the following command:

```bash
asreview --help
```

It should list the 'plot' subcommand and the 'stats' subcommand.

## Active learning performance 

The `ASReview-insights` extension is useful for measuring the performance of
active learning models on collections of binary labeled text. The extension
can be used after performing a simulation study that involves mimicking the
screening process with a specific model. As it is already known which records
are labeled relevant, the simulation can automatically reenact the screening
process as if a screener were using active learning. The performance of one or
multiple models can be measured by different metrics and the
`ASReview-insights` extension can plot or compute the values for such metrics
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

![ASReview metrics explained](https://github.com/asreview/asreview-insights/blob/master/stats_explainer.png)


## Plots

The plots in this section are derived from an ASReview (v1.0) file generated
from

```python
asreview simulate benchmark:van_de_schoot_2017 -s sim_van_de_schoot_2017.asreview --init_seed 535
```

### Plot types

#### Recall

The recall is an important metric to study the performance of active learning
algorithms in the context of information retrieval. ASReview Insights
offers a straightforward command line interface to plot a "recall curve". The
recall curve is the recall at any moment in the active learning process.

To plot the recall curve, you need a ASReview file (extension `.asreview`).
The file can be [exported from the ASReview LAB user interface](), or is the
[result of a simulation](). To plot the recall, use this syntax (Replace
`YOUR_ASREVIEW_FILE.asreview` by your ASReview file name.):

```bash
asreview plot recall YOUR_ASREVIEW_FILE.asreview
```

The following plot is the result of simulating the [`van_de_schoot_2017`](https://github.com/asreview/systematic-review-datasets/tree/master/datasets/van_de_Schoot_2017) in
the benchmark platform (command `asreview simulate
benchmark:van_de_schoot_2017 -s sim_van_de_schoot_2017.asreview`).

![Recall plot of Van de Schoot 2017](figures/tests_recall_sim_van_de_schoot_2017_1.png)

On the vertical axis, you find the recall (i.e, the proportion of the relevant
records) after every labeling decision. The horizontal axis shows the
proportion of  total number of records in the dataset. The steeper the recall
curve, the higher the performance of active learning when comparted to random
screening. The recall curve can also be used to estimate stopping criteria, see
the discussions in [#557](https://github.com/asreview/asreview/discussions/557) and [#1115](https://github.com/asreview/asreview/discussions/1115).


```bash
asreview plot recall YOUR_ASREVIEW_FILE.asreview
```

#### WSS

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

![Recall plot of Van de Schoot 2017](figures/tests_wss_default_sim_van_de_schoot_2017_1.png)

On the vertical axis, you find the WSS after every labeling decision. The
recall is displayed on the horizontal axis. As shown in the figure, the
WSS is linearly related to the recall.


#### ERF

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

![Recall plot of Van de Schoot 2017](figures/tests_erf_default_sim_van_de_schoot_2017_1.png)

On the vertical axis, you find the ERF after every labeling decision. The
horizontal axis shows the proportion of  total number of records in the
dataset. The steep increase of the ERF in the beginning of the process is
related to the steep recall curve.

### Very sparse datasets

Very sparse or small datasets can provide good explanation on interesting
details of the plotting subcommands in this extension. Important details are
for example the handling of prior knowledge and the computation of the recall
prediction in case of random screening.

The following plot shows the result of a collection of 4 records with 3
relevant items (inclusions). The relevant items are found in the following
order:

```
[1, 1, 0, 1, 0]
```

![Recall of small dataset example](figures/tests_small_dataset_recall.png)

The black line is an estimate of the recall after every screened record in a
naive manner (also refered to as 'random').

```
Recall (est) when screening 1 = (3 relevant records / 4 records left)  / 3 = 0.25
Recall (est) when screening 2 = (1/4) * (3 relevant records / 3 records left)  / 3 +
                                (3/4) * (2 relevant records / 3 records left)  / 3 = (1/4 + 3/4*2/3) / 3 = 0.25

```

The Work Saved over Sampling (WSS) is the difference between the recall of the
simulation and the theoretical recall of random screening.

![WSS for small dataset example](figures/tests_small_dataset_wss.png)

The following graph shows the recall versus the WSS. This comparison is
important because it is the fundamental of the `WSS@95%` metric used in the
literature about Active Learning for systematic reviewing.

![ERF for small dataset example](figures/tests_small_dataset_erf.png)


### Plotting CLI

See `asreview plot -h` for all command line arguments.

``` bash
% asreview plot -h
usage: asreview plot [-h] [--priors] [--no-priors] [--x_absolute] [--y_absolute] [-V] [-o OUTPUT]
                     type asreview_files [asreview_files ...]

positional arguments:
  type                  Plot type. Default 'recall'.
  asreview_files        A (list of) ASReview files.

optional arguments:
  -h, --help            show this help message and exit
  --priors              Include records used as prior knowledge in the plot.
  --no-priors           Exclude records used as prior knowledge in the plot. Default.
  --x_absolute          Make use of absolute coordinates on the x-axis.
  --y_absolute          Make use of absolute coordinates on the y-axis.
  -V, --version         show program's version number and exit
  -o OUTPUT, --output OUTPUT
                        Save the plot to a file. File formats are detected by the matplotlib library, check there to see available
                        formats.
```

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

![WSS with custom title](https://github.com/asreview/asreview-insights/blob/master/example_custom_title.png)

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

By default, all axes in ASReview-insights are relative. The API can be used to
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

![Recall with absolute axes](https://github.com/asreview/asreview-insights/blob/master/example_absolute_axes.png)


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
![Recall with multiple lines](https://github.com/asreview/asreview-insights/blob/master/example_multiple_lines.png)

## Metrics

The metrics in ASReview-insights can be used to extract metrics at given
values. The easiest way to get metrics on a ASReview project file is with the
following command don the command line:

```
asreview stats sim_van_de_schoot_2017.asreview
```

which results in

```
    "asreviewVersion": "1.0rc2+14.gac96c1a",
    "apiVersion": "1.0rc1+3.g19a776d.dirty",
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

Each available metric has two values. The first value is the value at
which the metric is computed. In the plots above, this is the x-axis. The
second value is the output of the metric. Some metrics are computed for multiple
values.

| Metric | Description pos. 1 | Description pos. 2 | Default |
|---|---|---|---|
| `recall` | Labels | Recall | 0.1, 0.25, 0.5, 0.75, 0.9 |
| `wss` | Recall | Work Saved over Sampling at recall | 0.95 |
| `erf` | Labels | ERF | 0.10 |


### Override default values

It is possible to override the default values of `asreview stats`. See
`asreview stats -h` for more information or see the example below.

```
asreview stats sim_van_de_schoot_2017.asreview --wss 0.9 0.95
```

```
{
    "asreviewVersion": "1.0rc2+14.gac96c1a",
    "apiVersion": "1.0rc1+3.g19a776d.dirty",
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
asreview stats sim_van_de_schoot_2017.asreview -o my_file.json
```

### Metrics CLI

See `asreview stats -h` for all command line arguments.

``` bash
% asreview stats -h
usage: asreview stats [-h] [-V] [--recall recall [recall ...]] [--wss wss [wss ...]] [--erf erf [erf ...]] [--priors] [--no-priors]
                      [--x_absolute] [--y_absolute] [-o OUTPUT]
                      asreview_files [asreview_files ...]

positional arguments:
  asreview_files        A combination of data directories or files.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  --recall recall [recall ...]
                        A (list of) values to compute the recall at.
  --wss wss [wss ...]   A (list of) values to compute the wss at.
  --erf erf [erf ...]   A (list of) values to compute the erf at.
  --priors              Include records used as prior knowledge in the metrics.
  --no-priors           Exclude records used as prior knowledge in the metrics. Default.
  --x_absolute          Make use of absolute coordinates on the x-axis.
  --y_absolute          Make use of absolute coordinates on the y-axis.
  -o OUTPUT, --output OUTPUT
                        Save the statistics and metrics to a JSON file.
```

### Metrics API

Metrics are easily accesible with the `ASReview-insights` API.

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

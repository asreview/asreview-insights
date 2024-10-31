# ASReview Insights

[![PyPI version](https://badge.fury.io/py/asreview-insights.svg)](https://badge.fury.io/py/asreview-insights) [![Downloads](https://pepy.tech/badge/asreview-insights)](https://pepy.tech/project/asreview-insights) ![PyPI - License](https://img.shields.io/pypi/l/asreview-insights) ![Deploy and release](https://github.com/asreview/asreview-insights/workflows/Deploy%20and%20release/badge.svg) ![Build status](https://github.com/asreview/asreview-insights/workflows/test-suite/badge.svg) [![DOI](https://zenodo.org/badge/235795131.svg)](https://zenodo.org/badge/latestdoi/235795131)


This official extension to [ASReview
LAB](https://github.com/asreview/asreview) extends the software with tools for
[plotting](#plot-types) and extracting the [statistical results](#metrics) of
several [performance metrics](#performance-metrics). The extension is
especially useful in combination with the [simulation
functionality](https://asreview.readthedocs.io/en/latest/simulation_overview.html)
of ASReview LAB.

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
multiple models can be measured by different metrics and the ASReview Insights
extension can plot or compute the values for such metrics from ASReview
project files. [O'Mara-Eves et al.
(2015)](https://doi.org/10.1186/2046-4053-4-5) provides a comprehensive
overview of different metrics used in the field of actrive learning. Below we
describe the metrics available in the software.

### Recall

The recall is the proportion of relevant records that have been found at a
certain point during the screening phase. It is sometimes also called the
proportion of Relevant Record Found (RRF) after screening an X% of the total
records. For example, the RRF@10 is the recall (i.e., the proportion of the
total number of relevant records) at screening 10% of the total number of
records available in the dataset.

### Confusion matrix

The confusion matrix consist of the True Positives (TP), False Positives (FP),
True Negatives (TN), and False Negatives (FN). Definitions are provided in the
following table retrieved at a certain recall (r%).

|                      | Definition                                                                             | Calculation                     |
|----------------------|----------------------------------------------------------------------------------------|---------------------------------|
| True Positives (TP)  | The number of relevant records found at recall level                                   | Relevant Records * r%           |
| False Positives (FP) | The number of irrelevant records reviewed at recall level                              | Records Reviewed – TP           |
| True Negatives (TN)  | The number of irrelevant records correctly not reviewed at recall level                | Irrelevant Records – FP         |
| False Negatives (FN) | The number of relevant records not reviewed at recall level (missing relevant records) | Relevant Records – TP           |

### Work saved over sampling

The Work Saved over Sampling (WSS) is a measure of "the work saved over and
above the work saved by simple sampling for a given level of recall" [(Cohen
et al., 2006)](https://doi.org/10.1197/jamia.m1929). It is defined as the
proportion of records a screener does **not** have to screen compared to
random reading after providing the prior knowledge used to train the first
iteration of the model. The WSS is typically measured at a recall of .95
(WSS@95), reflecting the proportion of records saved by using active learning
at the cost of failing to identify .05 of relevant publications.

[Kusa et al. (2023)](https://doi.org/10.1016/j.iswa.2023.200193) propose to
normalize the WSS for class imbalance (denoted as the nWSS). Moreover, Kusa et
al. showed that nWSS is equal to the True Negative Rate (TNR). The TNR is the
proportion of irrelevant records that were correctly not reviewed at level of
recall. The nWSS is useful to compare performance in terms of work saved
across datasets and models while controlling for dataset class imbalance.

The following table provides a hypothetical dataset example:

| Dataset characteristics | Example value     |
|-------------------------|-------------------|
| Total records           | 2000              |
| Records Reviewed        | 1100              |
| Relevant Records        | 100               |
| Irrelevant Records      | 1900              |
| Class imbalance         | 5%                |

With this information, the following metrics can be calculated:

| Metric   | Example value     |
|----------|-------------------|
| TP       | 95                |
| FP       | 1100 – 95 = 1005  |
| TN       | 1900 – 1005 = 895 |
| FN       | 100 – 95 = 5      |
| TNR95%   | 895 / 1900 = 0.47 |


### Extra relevant found

A variation is the Extra Relevant records Found (ERF), which is the proportion
of relevant records found after correcting for the number of relevant records
found via random screening (assuming a uniform distribution of relevant
records).

The following plot illustrates the differences between the metrics Recall
(y-axis), WSS (blue line), and ERF (red line). The dataset contains 1.000
hypothetical records with labels. The stepped line on the diagonal is the
naive labeling approach (screening randomly sorted records).

![ASReview metrics explained](https://github.com/asreview/asreview-insights/blob/main/docs/stats_explainer.png)

### Time to discovery

Both recall and WSS are sensitive to the position of the cutoff value and the
distribution of the data. Moreover, the WSS makes assumptions about the
acceptable recall level whereas this level might depend on the research
question at hand. Therefore, [Ferdinands et al.
(2020)](https://doi.org/10.1186/s13643-023-02257-7) proposed two new metrics:
(1) the Time to Discover a relevant record as the fraction of records needed
to screen to detect this record (TD); and (2) the Average Time to Discover
(ATD) as an indicator of how many records need to be screened on average to
find all relevant records in the dataset. The TD metric enables you to
pinpoint hard-to-find papers. The ATD, on the other hand, measures performance
throughout the entire screening process, eliminating reliance on arbitrary
cut-off values, and can be used to compare different models.

### Loss
The Loss metric evaluates the performance of an active learning model by
quantifying how closely it approximates the ideal screening process. This
quantification is then normalized between the ideal curve and the worst possible
curve.

While metrics like WSS, Recall, and ERF evaluate the performance at specific
points on the recall curve, the Loss metric provides an overall measure of
performance.

To compute the loss, we start with three key concepts:

1. **Optimal AUC**: This is the area under a "perfect recall curve," where
   relevant records are identified as early as possible. Mathematically, it is
   computed as $Nx \times Ny - \frac{Ny \times (Ny - 1)}{2}$, where $Nx$ is the
   total number of records, and $Ny$ is the number of relevant records.

2. **Worst AUC**: This represents the area under a worst-case recall curve,
   where all relevant records appear at the end of the screening process. This
   is calculated as $\frac{Ny \times (Ny + 1)}{2}$.

3. **Actual AUC**: This is the area under the recall curve produced by the model
   during the screening process. It can be obtained by summing up the cumulative
   recall values for the labeled records.

The normalized loss is calculated by taking the difference between the optimal
AUC and the actual AUC, divided by the difference between the optimal AUC and
the worst AUC.

$$\text{Normalized Loss} = \frac{Ny \times \left(Nx - \frac{Ny - 1}{2}\right) -
\sum \text{Cumulative Recall}}{Ny \times (Nx - Ny)}$$

The lower the loss, the closer the model is to the perfect recall curve,
indicating higher performance.

![Recall plot illustrating loss metric](https://github.com/asreview/asreview-insights/blob/main/figures/loss_metric_example.png?raw=true)

In this figure, the green area between the recall curve and the perfect recall line is the lost performance, which is then normalized for the total area (green and red combined).

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

To plot the recall curve, you need a ASReview file (extension `.asreview`). To
plot the recall, use this syntax (Replace `YOUR_ASREVIEW_FILE.asreview` by
your ASReview file name.):

```bash
asreview plot recall YOUR_ASREVIEW_FILE.asreview
```

The following plot is the result of simulating the [`PTSD data`](https://doi.org/10.1038/s42256-020-00287-7) via
the benchmark platform (command `asreview simulate
benchmark:van_de_schoot_2017 -s sim_van_de_schoot_2017.asreview`).

![Recall plot of Van de Schoot 2017](https://github.com/asreview/asreview-insights/blob/main/figures/tests_recall_sim_van_de_schoot_2017_stop_if_min.png)

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

The Work Saved over Sampling (WSS) metric is a useful metric to study the
performance of active learning alorithms compared with a naive (random order)
approach at a given level of recall. ASReview Insights offers a
straightforward command line interface to plot the WSS at any level of recall.

To plot the WSS curve, you need a ASReview file (extension `.asreview`). To
plot the WSS, use this syntax (Replace `YOUR_ASREVIEW_FILE.asreview` by your
ASReview file name.):

```bash
asreview plot wss YOUR_ASREVIEW_FILE.asreview
```

The following plot is the result of simulating the [`PTSD data`](https://doi.org/10.1038/s42256-020-00287-7) via
the benchmark platform (command `asreview simulate
benchmark:van_de_schoot_2017 -s sim_van_de_schoot_2017.asreview`).

![Recall plot of Van de Schoot 2017](https://github.com/asreview/asreview-insights/blob/main/figures/tests_wss_default_sim_van_de_schoot_2017_stop_if_min.png)

On the vertical axis, you find the WSS after every labeling decision. The
recall is displayed on the horizontal axis. As shown in the figure, the
WSS is linearly related to the recall.


#### `erf`

The Extra Relevant Records found is a derivative of the recall and presents
the proportion of relevant records found after correcting for the number of
relevant records found via random screening (assuming a uniform distribution
of relevant records).

To plot the ERF curve, you need a ASReview file (extension `.asreview`). To
plot the ERF, use this syntax (Replace `YOUR_ASREVIEW_FILE.asreview` by your
ASReview file name.):


```bash
asreview plot erf YOUR_ASREVIEW_FILE.asreview
```
The following plot is the result of simulating the [`PTSD data`](https://doi.org/10.1038/s42256-020-00287-7) via
the benchmark platform (command `asreview simulate
benchmark:van_de_schoot_2017 -s sim_van_de_schoot_2017.asreview`).

![Recall plot of Van de Schoot 2017](https://github.com/asreview/asreview-insights/blob/main/figures/tests_erf_default_sim_van_de_schoot_2017_stop_if_min.png)

On the vertical axis, you find the ERF after every labeling decision. The
horizontal axis shows the proportion of  total number of records in the
dataset. The steep increase of the ERF in the beginning of the process is
related to the steep recall curve.

### Plotting CLI

Optional arguments for the command line are `--priors` to include prior
knowledge, `--x_absolute` and `--y_absolute` to use absolute axes.

See `asreview plot -h` for all command line arguments.

### Plotting multiple files
It is possible to show the curves of multiple files in one plot. Use this
syntax (replace `YOUR_ASREVIEW_FILE_1` and `YOUR_ASREVIEW_FILE_2` by the
asreview_files that you want to include in the plot):

```bash
asreview plot recall YOUR_ASREVIEW_FILE_1.asreview YOUR_ASREVIEW_FILE_2.asreview
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

![WSS with custom title](https://github.com/asreview/asreview-insights/blob/main/docs/example_custom_title.png)

#### Example: Prior knowledge

It's possible to include prior knowledge in your plot. By default, prior
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

![Recall with absolute
axes](https://github.com/asreview/asreview-insights/blob/main/docs/example_absolute_axes.png)

#### Example: Adjusting the random and optimal recalls

By default, each plot will have a curve representing optimal performance, and a
curve representing random sampling performance. Both curves can be removed from
the graph.

```python
import matplotlib.pyplot as plt
from asreview import open_state

from asreviewcontrib.insights.plot import plot_recall

with open_state("example.asreview") as s:

    fig, ax = plt.subplots()
    plot_recall(ax, s, show_random=False, show_optimal=False)

    fig.savefig("example_without_curves.png")
```

![Recall with absolute axes](https://github.com/asreview/asreview-insights/blob/main/docs/example_without_curves.png)


#### Example: Legend for multiple curves in one plot

If you have multiple curves in one plot, you can customize the legend:

```python
import matplotlib.pyplot as plt

from asreview import open_state
from asreviewcontrib.insights.plot import plot_recall


fig, ax = plt.subplots()

with open_state("tests/asreview_files/sim_van_de_schoot_2017_1.asreview") as s1:
    with open_state("tests/asreview_files/"
                    "sim_van_de_schoot_2017_logistic.asreview") as s2:
        plot_recall(ax,
                    [s1, s2],
                    legend_values=["Naive Bayes", "Logistic"],
                    legend_kwargs={'loc': 'lower center'})

fig.savefig("docs/example_multiple_lines.png")

```
![Recall with multiple lines](https://github.com/asreview/asreview-insights/blob/main/docs/example_multiple_lines.png)

## `metrics`

The `metrics` subcommand in ASReview Insights can be used to compute metrics
at given values. The easiest way to compute metrics for a ASReview project
file is with the following command on the command line:

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
                "id": "loss",
                "title": "Loss",
                "value": 0.01707543880041846
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
            },
            {
                "id": "atd",
                "title": "Average time to discovery",
                "value": 101.71428571428571
            },
            {
                "id": "td",
                "title": "Time to discovery",
                "value": [
                    [
                        3898,
                        22
                    ],
                    [
                        284,
                        23
                    ],
                    [
                        592,
                        25
                    ],
                    ...
                    [
                        2382,
                        184
                    ],
                    [
                        5479,
                        224
                    ],
                    [
                        3316,
                        575
                    ]
                ]
            },
            {
                "id": "tp",
                "title": "True Positives",
                "value": [
                    [
                        0.95,
                        39
                    ],
                    [
                        1.0,
                        42
                    ]
                ]
            },
            {
                "id": "fp",
                "title": "False Positives",
                "value": [
                    [
                        0.95,
                        122
                    ],
                    [
                        1.0,
                        517
                    ]
                ]
            },
            {
                "id": "tn",
                "title": "True Negatives",
                "value": [
                    [
                        0.95,
                        6023
                    ],
                    [
                        1.0,
                        5628
                    ]
                ]
            },
            {
                "id": "fn",
                "title": "False Negatives",
                "value": [
                    [
                        0.95,
                        3
                    ],
                    [
                        1.0,
                        0
                    ]
                ]
            },
            {
                "id": "tnr",
                "title": "True Negative Rate (Specificity)",
                "value": [
                    [
                        0.95,
                        0.980146
                    ],
                    [
                        1.0,
                        0.915867
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
| `atd` | Average time to discovery (in label actions) | - | - |
| `td` | Row number (starting at 0) | Number of records labeled | - |
| `cm` | Recall  | Confusion matrix values at recall | 0.95, 1 |


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
            },
            {
                "id": "atd",
                "title": "Average time to discovery",
                "value": 101.71428571428571
            },
            {
                "id": "td",
                "title": "Time to discovery",
                "value": [
                    [
                        3898,
                        22
                    ],
                    [
                        284,
                        23
                    ],
                    [
                        592,
                        25
                    ],
                    ...
                    [
                        2382,
                        184
                    ],
                    [
                        5479,
                        224
                    ],
                    [
                        3316,
                        575
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
knowledge, `--x_absolute` and `--y_absolute` to use absolute axes.

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

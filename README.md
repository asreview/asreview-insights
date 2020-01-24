## ASReview-visualization

This is a plotting/visualization supplemental package for the 
[ASReview](https://github.com/msdslab/automated-systematic-review)
software. It is a fast way to create a visual impression of the ASReview with different
dataset, models and model parameters.

### Installation

The easiest way to install the visualization package is to use the command line:

``` bash
pip install git+https://github.com/msdslab/ASReview-visualization.git
```

### Basic usage

After installation of the visualization package, asreview should automatically detect it.
Test this by:

```bash
asreview --help
```

It should list the 'plot' modus.

Log files that were created with the same ASReview settings can be put together/averaged by putting
them in the same directory. Log files with different settings/datasets should be put in different 
directories to compare them. It is advised to put these log files in the same directory.

As an example consider the following directory structure, where we have two datasets, called `ace` and
`ptsd`, each of which have 8 runs:

```
├── ace
│   ├── results_0.h5
│   ├── results_1.h5
│   ├── results_2.h5
│   ├── results_3.h5
│   ├── results_4.h5
│   ├── results_5.h5
│   ├── results_6.h5
│   └── results_7.h5
└── ptsd
    ├── results_0.h5
    ├── results_1.h5
    ├── results_2.h5
    ├── results_3.h5
    ├── results_4.h5
    ├── results_5.h5
    ├── results_6.h5
    └── results_7.h5
```

Then we can plot the results by:

```bash
asreview plot ace ptsd
```

By default, the values shown are expressed as percentages of the total number of papers. Use the
`-a` or `--absolute-values` flags to have them expressed in absolute numbers:

```bash
asreview plot ace ptsd --absolute-values
```


### Plot types

There are currently three plot types implemented: _inclusions_, _discovery_, _limits_. They can be
individually selected with the `-t` or `--type` switch. Multiple plots can be made by using `,` as
a separator:

```bash
asreview plot ace ptsd --type 'inclusions,discovery'
```

#### Inclusions

This figure shows the number/percentage of included papers found as a function of the
number/percentage of papers reviewed. Initial included/excluded papers are subtracted so that the line
always starts at (0,0).

The quicker the line goes to a 100%, the better the performance.

![alt text](docs/inclusions.png?raw=true "Inclusions")

#### Discovery

This figure shows the distribution of the number of papers that have to be read before discovering
each inclusion. Not every paper is equally hard to find.

The closer to the left, the better.

![alt text](docs/discovery.png?raw=true "Discovery")


#### Limits

This figure shows how many papers need to be read with a given criterion. A criterion is expressed
as "after reading _y_ % of the papers, at most an average of _z_ included papers have been not been
seen by the reviewer, if he is using max sampling.". Here, _y_ is shown on the y-axis, while
three values of _z_ are plotted as three different lines with the same color. The three values for
_z_ are 0.1, 0.5 and 2.0.

The quicker the lines touch the black (`y=x`) line, the better.

![alt text](docs/limits.png?raw=true "Limits")

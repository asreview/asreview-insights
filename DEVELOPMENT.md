# Development

## Very sparse datasets

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

![Recall of small dataset example](https://github.com/asreview/asreview-insights/blob/master/figures/tests_small_dataset_recall.png)

The black line is an estimate of the recall after every screened record in a
naive manner (also refered to as 'random').

The Work Saved over Sampling (WSS) is the difference between the recall of the
simulation and the theoretical recall of random screening.

![WSS for small dataset example](https://github.com/asreview/asreview-insights/blob/master/figures/tests_small_dataset_wss.png)

The following graph shows the recall versus the WSS. This comparison is
important because it is the fundamental of the `WSS@95%` metric used in the
literature about Active Learning for systematic reviewing.

![ERF for small dataset example](https://github.com/asreview/asreview-insights/blob/master/figures/tests_small_dataset_erf.png)

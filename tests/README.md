# Testing ASReview-insights

## Create ASReview files

```
asreview simulate benchmark:van_de_schoot_2017 -s sim_van_de_schoot_2017_stop_if_min.asreview --init_seed 535 --seed 400 --stop_if min
asreview simulate benchmark:van_de_schoot_2017 -s sim_van_de_schoot_2017_stop_if_full.asreview --init_seed 535 --seed 400 --stop_if -1
```

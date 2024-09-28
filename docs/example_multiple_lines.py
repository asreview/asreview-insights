# An example of plotting the recall curves for two ASREVIEW files in one plot,
# with a legend.

import matplotlib.pyplot as plt
from asreview import open_state

from asreviewcontrib.insights.plot import plot_recall

fig, ax = plt.subplots()

with open_state(
    "tests/asreview_files/sim_van_de_schoot_2017_stop_if_min.asreview"
) as s1:
    plot_recall(ax, s1)

with open_state(
    "tests/asreview_files/" "sim_van_de_schoot_2017_logistic.asreview"
) as s2:
    plot_recall(ax, s2)

# Set the labels for the legend. Both plots add the recall line, the random
# curve, and the optimal recall. Hence the recall lines are the 0th and 3nd line.
ax.lines[0].set_label("Naive Bayes")
ax.lines[3].set_label("Logistic")
ax.legend()

fig.savefig("docs/example_multiple_lines.png")

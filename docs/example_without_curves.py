import matplotlib.pyplot as plt
from asreview import open_state

from asreviewcontrib.insights.plot import plot_recall

with open_state("tests/asreview_files/sim_van_de_schoot_2017_logistic.asreview") as s:
    fig, ax = plt.subplots()
    plot_recall(ax, s, show_random=False, show_optimal=False)

    fig.savefig("docs/example_without_curves.png")

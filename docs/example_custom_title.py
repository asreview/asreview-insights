import matplotlib.pyplot as plt
from asreview import open_state

from asreviewcontrib.insights.plot import plot_wss

with open_state("tests/asreview_files/sim_van_de_schoot_2017_logistic.asreview") as s:
    fig, ax = plt.subplots()

    plot_wss(ax, s)

    plt.title("WSS with custom title")

    fig.savefig("docs/example_custom_title.png")

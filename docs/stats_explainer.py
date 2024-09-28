"""Create example plot with different metrics.

Example
-------

python docs/stats_explainer.py
"""

import matplotlib.pyplot as plt
import numpy as np

from asreviewcontrib.insights.plot import _fix_start_tick

# The recall at a given number of documents read is the fraction of the
# relevant records found at that moment. (recall = n_pos_records / n_records)

# The old RRF@X (relevant records found) is basically the same as the recall.

# The WSS@X (work saved over sampling) is the number of records you need to
# read less to find the fraction X of relevant records. (wss = recall - recall_random)

# The (my suggestion for a name) ERF@X (extra records found) is the number of
# extra relevant records found after reading a fraction X of the total number of
# records.

# Create fictive data.
n_docs = 1000
n_pos_docs = 30

percentages = np.array([x ** (1 / 3) for x in np.linspace(0, 1, n_docs)])
n_docs_found = np.round(percentages * n_pos_docs)
labels = [
    n_docs_found[i + 1] - n_docs_found[i] for i in range(len(n_docs_found) - 1)
] + [0]
labels[0] = 1
labels[5] = 1
labels[8] = 1

# Plot the recall curve.
fig, ax = plt.subplots()

x = list(range(1, n_docs + 1))

# Recall curve.
recall = np.cumsum(labels) / np.sum(labels)
ax.step(x, recall, where="post")

# Random
recall_random = np.round(np.linspace(0, n_pos_docs, n_docs)) / np.sum(labels)
ax.step(x, recall_random, where="post", color="black")

# Add the ERF@.137 line (recall > 0.5 at 137, recall_random 0.5 at 517).
ax.plot((137, 137), (137 / 1000, recall[137]), color="red")
erf_x_offset = -70
ax.text(137 + erf_x_offset, (137 / 1000 + recall[137]) * 0.9 / 2, "ERF", color="red")
# Add the WSS@.5 line.
ax.plot((137, 517), (recall[137], recall[137]), color="blue")
wss_y_offset = 0.03
ax.text((137 + recall[137] * 1000) / 2, recall[137] + wss_y_offset, "WSS", color="blue")

ax.set_title("Explaining Recall, WSS and ERF")
ax.set(xlabel="#", ylabel="Recall")
ax.set_ylim([-0.05, 1.05])
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.xaxis.get_major_locator().set_params(integer=True)

_fix_start_tick(ax)

fig.savefig("docs/stats_explainer.png")

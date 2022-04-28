import matplotlib.pyplot as plt


def _fix_start_tick(ax):

    # correct x axis if tick is at position 0
    locs = ax.get_xticks()
    if locs[1] == 0:
        locs[1] = 1
        ax.set_xticks(locs[1:-1])

    return ax
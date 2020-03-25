def inclusion_plot(plot, **kwargs):
    all_files = all(plot.is_file.values())
    if all_files:
        thick = {key: True for key in list(plot.analyses)}
    else:
        thick = None

    inc_plot = plot.new("inclusions", thick=thick, **kwargs)
    inc_plot.set_grid()

    for key in list(plot.analyses):
        if all_files or not plot.is_file[key]:
            inc_plot.add_WSS(key, 95)
            inc_plot.add_WSS(key, 100)
            inc_plot.add_RRF(key, 5)
    inc_plot.add_random()
    inc_plot.set_legend()
    inc_plot.show()


def progression_plot(plot, **kwargs):
    all_files = all(plot.is_file.values())
    if all_files:
        thick = {key: True for key in list(plot.analyses)}
    else:
        thick = None

    inc_plot = plot.new("progression", thick=thick, **kwargs)
    inc_plot.set_grid()
    inc_plot.set_legend()
    inc_plot.show()

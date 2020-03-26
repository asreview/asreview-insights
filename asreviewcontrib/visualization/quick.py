def inclusion_plot(plot, output=None, **kwargs):
    all_files = all(plot.is_file.values())

    inc_plot = plot.new("inclusion", **kwargs)
    inc_plot.set_grid()

    for key in list(plot.analyses):
        if all_files or not plot.is_file[key]:
            inc_plot.add_WSS(key, 95)
            inc_plot.add_WSS(key, 100)
            inc_plot.add_RRF(key, 5)
    inc_plot.add_random()
    inc_plot.set_legend()
    if output is None:
        inc_plot.show()
    else:
        inc_plot.save(output)


def progression_plot(plot, output=None, **kwargs):
    prog_plot = plot.new("progression", **kwargs)
    prog_plot.set_grid()
    prog_plot.set_legend()
    if output is None:
        prog_plot.show()
    else:
        prog_plot.save(output)


def discovery_plot(plot, output=None, **kwargs):
    disc_plot = plot.new("discovery", **kwargs)
    disc_plot.set_legend()
    if output is None:
        disc_plot.show()
    else:
        disc_plot.save(output)


def limit_plot(plot, output=None, **kwargs):
    limit_plot = plot.new("limit", **kwargs)
    limit_plot.set_legend()
    limit_plot.set_grid()
    if output is None:
        limit_plot.show()
    else:
        limit_plot.save(output)

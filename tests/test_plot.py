import os
from pathlib import Path

from pytest import mark

from asreview import review_simulate

from asreviewcontrib.visualization.entrypoint import PlotEntryPoint


def create_state_file(data_fp, state_fp):
    try:
        os.remove(state_fp)
    except FileNotFoundError:
        pass

    review_simulate(str(data_fp), state_file=state_fp, n_prior_included=1,
                    n_prior_excluded=1, model="nb",
                    feature_extraction="tfidf")


def plot_setup(data_fp, state_dirs, state_files):
    for dir_ in state_dirs:
        os.makedirs(dir_, exist_ok=True)
    for file_ in state_files:
        create_state_file(data_fp, file_)


def plot_clean(dirs, files):
    for f in files:
        try:
            os.remove(f)
        except FileNotFoundError:
            pass
    for d in dirs:
        try:
            os.rmdir(d)
        except (FileNotFoundError, OSError):
            pass


COMBINATIONS = [
    (pt, numbers)
    for pt in ["inclusion", "progress", "discovery", "limit"]
    for numbers in [True, False]
]


@mark.parametrize(
    "plot_type,numbers", COMBINATIONS
)
def test_plots(request, plot_type, numbers):
    test_dir = request.fspath.dirname
    output_dir = Path(test_dir, "output")
    state_dirs = [Path(output_dir, x) for x in ["h5", "json"]]
    h5_dir = Path(output_dir, "h5")
    json_dir = Path(output_dir, "json")
    h5_files = [Path(output_dir, "h5", f"result_{x}.h5") for x in [1, 2]]
    json_files = [Path(output_dir, "json", f"result_{x}.json") for x in [1, 2]]
    data_fp = Path(test_dir, "data", "embase_labelled.csv")
    picture_fp = Path(output_dir, "test.png")

    if (plot_type, numbers) == COMBINATIONS[0]:
        plot_setup(data_fp, state_dirs+[output_dir], h5_files+json_files)

    data_combis = [
        [h5_dir, *h5_files],
        [json_dir, *json_files],
        [h5_dir, json_dir],
    ]
    for combi in data_combis:
        try:
            os.remove(picture_fp)
        except FileNotFoundError:
            pass
        args = [*[str(x) for x in combi], "-o", str(picture_fp)]
        if numbers:
            args += ["--absolute-values"]
        entry = PlotEntryPoint()
        entry.execute(args)
        assert os.path.isfile(picture_fp)

    if (plot_type, numbers) == COMBINATIONS[-1]:
        plot_clean(state_dirs + [output_dir],
                   h5_files + json_files + [picture_fp])

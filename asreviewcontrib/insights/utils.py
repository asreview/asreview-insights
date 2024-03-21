from pathlib import Path

import numpy as np
from asreview import open_state
from asreview.state import SQLiteState


def _pad_simulation_labels(state_obj, priors=False):
    """Get the labels from state file(s).

    Parameters
    ----------
    state_obj : (list of) asreview.state.SQLiteState
        Single state object, or list of multiple state objects.
    priors : bool, optional
        Include the prior labels, by default False

    Returns
    -------
    list or list of lists
        List of labels if state_obj is a single state. List of lists of labels
        if state_obj is a list of states.
    """
    if isinstance(state_obj, SQLiteState):
        # get the number of records
        n_records = state_obj.n_records

        # get the labels
        labels = state_obj.get_labels(priors=priors).to_list()

        if not priors:
            n_used_records = n_records - state_obj.n_priors
        else:
            n_used_records = n_records

        # if less labels than records, check if all labels available
        if len(labels) < n_used_records:
            labels = labels + np.zeros(n_used_records - len(labels)).tolist()

        return labels
    else:
        return [
            _pad_simulation_labels(single_state, priors) for single_state in state_obj
        ]


def _iter_states(file_paths):
    """Get a generator of state objects from their filepaths.

    Parameters
    ----------
    file_paths : list[Path]
        List of filepaths of states.

    Yields
    ------
    asreview.state.BaseState
        State at given filepath.
    """
    for fp in file_paths:
        with open_state(fp) as s:
            yield s


def _get_files(asreview_files):
    return [
        str(file)
        for path in asreview_files
        for file in (Path(path).glob("*.asreview") if Path(path).is_dir() else [Path(path)])  # noqa
    ]


def _legend_values(asreview_files, state_obj, legend_option):
    legend_values = []

    for state_file_path, state in zip(asreview_files, state_obj):
        metadata = state.settings_metadata
        label = None

        if legend_option == "filename":
            label = Path(state_file_path).stem
        elif legend_option == "model":
            label = " - ".join(
                [metadata["settings"]["model"],
                 metadata["settings"]["feature_extraction"],
                 metadata["settings"]["balance_strategy"],
                 metadata["settings"]["query_strategy"]])
        elif legend_option == "classifier":
            label = metadata["settings"]["model"]
        else:
            raise ValueError(f"Invalid legend setting: '{legend_option}'")

        legend_values.append(label)

    return legend_values

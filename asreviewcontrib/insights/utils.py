import numpy as np
from asreview import SQLiteState
from asreview import open_state


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
        n_records = len(state_obj.get_last_ranking_table())

        # get the labels
        labels = state_obj.get_results_table(columns="label", priors=priors)[
            "label"
        ].to_list()

        if not priors:
            n_used_records = n_records - len(state_obj.get_priors())
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

import numpy as np
from asreview import open_state

from pathlib import Path


def get_labels(state_obj, priors=False):

    # get the number of records
    n_records = state_obj.n_records

    # get the labels
    labels = state_obj.get_labels(priors=priors).to_list()

    # if less labels than records, check if all labels available
    if len(labels) < n_records:

        labels = labels + np.zeros(n_records - len(labels)).tolist()

    return labels


def get_multiple_labels(fps, priors=False):
    """Get the labels from multiple state files.

    Parameters
    ----------
    fps : list[Path]
        List of filepaths of ASReview project files.
    priors : bool, optional
        Also get the labels for the priors, by default False

    Returns
    -------
    dict[list]
        Dictionary {project_name: labels}
    """
    multiple_labels = {}
    for fp in fps:
        fp = Path(fp)
        project_name = fp.stem
        with open_state(fp) as state:
            multiple_labels[project_name] = get_labels(state, priors)
    return multiple_labels

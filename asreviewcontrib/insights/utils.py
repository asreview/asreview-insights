import tempfile

import numpy as np
from asreview import Project
from asreview import open_state


def get_simulation_labels(asreview_file, priors=False):
    """Get the list of labels from an asreview file.

    Parameters
    ----------
    asreview_file : str | Path
        Path to an asreview file.
    priors : bool, optional
        Include the prior labels, by default False

    Returns
    -------
    list[0 | 1]
        List of labels (0 or 1) from an asreview file. If `priors=False`, the labels of
        the prior records are skipped.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        project = Project.load(asreview_file=asreview_file, project_path=tmpdir)
        n_records = len(project.data_store)

    with open_state(asreview_file) as state_obj:
        # get the labels
        labels = state_obj.get_results_table(columns="label", priors=priors)[
            "label"
        ].to_list()
        if priors:
            n_priors_to_skip = 0
        else:
            n_priors_to_skip = len(state_obj.get_priors())

    n_used_records = n_records - n_priors_to_skip

    # if less labels than records, check if all labels available
    if len(labels) < n_used_records:
        labels = labels + np.zeros(n_used_records - len(labels)).tolist()

    return labels

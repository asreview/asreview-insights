import numpy as np


def pad_simulation_labels(state_obj, priors=False):

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

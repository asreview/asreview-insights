import numpy as np


def _recall_values(labels, x_absolute=False, y_absolute=False):
    n_docs = len(labels)
    n_pos_docs = sum(labels)

    x = np.arange(1, n_docs + 1)
    recall = np.cumsum(labels)

    if not x_absolute:
        x = x / n_docs

    if y_absolute:
        y = recall
    else:
        y = recall / n_pos_docs

    return x.tolist(), y.tolist()


def _wss_values(labels, x_absolute=False, y_absolute=False):
    n_docs = len(labels)
    n_pos_docs = sum(labels)

    docs_found = np.cumsum(labels)
    docs_found_random = np.round(np.linspace(0, n_pos_docs, n_docs))

    # Get the first occurrence of 1, 2, 3, ..., n_pos_docs in both arrays.
    when_found = np.searchsorted(docs_found, np.arange(1, n_pos_docs + 1))
    when_found_random = np.searchsorted(docs_found_random,
                                        np.arange(1, n_pos_docs + 1))
    n_found_earlier = when_found_random - when_found

    x = np.arange(1, n_pos_docs + 1)
    if not x_absolute:
        x = x / n_pos_docs

    if y_absolute:
        y = n_found_earlier
    else:
        y = n_found_earlier / n_docs

    return x.tolist(), y.tolist()


def _erf_values(labels, x_absolute=False, y_absolute=False):

    n_docs = len(labels)
    n_pos_docs = sum(labels)

    docs_found = np.cumsum(labels)
    docs_found_random = np.round(np.linspace(0, n_pos_docs, n_docs))

    extra_records_found = docs_found - docs_found_random

    x = np.arange(1, n_docs + 1)
    if not x_absolute:
        x = x / n_docs

    if y_absolute:
        y = extra_records_found
    else:
        y = extra_records_found / n_pos_docs

    return x.tolist(), y.tolist()


def _confusion_matrix_values(labels,x_absolute=False):    
    
    n_relevant = int(sum(labels)) #n total relevant recs
    n_irrelevant= labels.count(0) #n total irrelevant recs    
    n_docs = len(labels) #n records 
    screened  = np.arange(1,n_docs+1) 
      
    n_tp = np.cumsum(labels,dtype=int) #TP             
    n_fp = screened - n_tp #FP (#screened - TP) #incorrectly predicted as include
    n_tn = n_irrelevant - n_fp #TN (#irrelevant - FP) correclty predicted as exclude (did not have to screen)
    n_fn = n_relevant - n_tp #FN (#relevant - TP)  #missing relevant recs
    
    if not x_absolute:
        screened = screened/n_docs # recs screened
    else:
        screened  = screened  
  
    return screened.tolist(),n_tp.tolist(), n_fp.tolist(), n_tn.tolist(), n_fn.tolist()



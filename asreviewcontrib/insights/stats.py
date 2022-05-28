import json

import asreview

from asreviewcontrib.insights.metrics import _erf
from asreviewcontrib.insights.metrics import _recall
from asreviewcontrib.insights.metrics import _wss


def get_stats(state_obj,
              recall=[0.1, 0.25, 0.5, 0.75, 0.9],
              wss=[0.95],
              erf=[0.10],
              priors=False,
              x_absolute=False,
              y_absolute=False,
              version=None):

    recall = [recall] if not isinstance(recall, list) else recall
    wss = [wss] if not isinstance(wss, list) else wss
    erf = [erf] if not isinstance(erf, list) else erf

    labels = state_obj.get_labels(priors=priors).to_list()

    recall_values = [
        _recall(labels, v, x_absolute=x_absolute, y_absolute=y_absolute)
        for v in recall
    ]
    wss_values = [
        _wss(labels, v, x_absolute=x_absolute, y_absolute=y_absolute)
        for v in wss
    ]
    erf_values = [
        _erf(labels, v, x_absolute=x_absolute, y_absolute=y_absolute)
        for v in erf
    ]

    # based on https://google.github.io/styleguide/jsoncstyleguide.xml
    result = {
        "asreviewVersion": asreview.__version__,
        "apiVersion": version,
        "data": {
            "items": [{
                "id": "recall",
                "title": "Recall",
                "value": [(i,v) for i, v in zip(recall, recall_values)]
            }, {
                "id": "wss",
                "title": "Work Saved over Sampling",
                "value": [(i,v) for i, v in zip(wss, wss_values)]
            }, {
                "id": "erf",
                "title": "Extra Relevant record Found",
                "value": [(i,v) for i, v in zip(erf, erf_values)]
            }]
        }
    }

    return result


def print_stats(stats):

    print(json.dumps(stats, indent=4))

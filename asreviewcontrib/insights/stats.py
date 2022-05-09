import json


def get_stats():

    result = {
        "metrics": {
            "wss": [{
                "type": "recall",
                "valueType": 0.95,
                "value": None
            }],
            "rrf": [{
                "valueType": 0.1,
                "value": None
            }]
        }
    }

    return result


def print_stats(stats):

    print(json.dumps(stats, indent=4))

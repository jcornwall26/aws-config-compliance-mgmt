import json
from notifications_handler.handler import lambda_handler

def _load_from_file():
    with open("tests/event_example.json") as json_file:
        return json.load(json_file)

def test_handler():
    result = lambda_handler(_load_from_file(), None)

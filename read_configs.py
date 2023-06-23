import json

def read_environment():
    with open('environment.json', 'r') as f:
        configs = json.load(f)
    return configs

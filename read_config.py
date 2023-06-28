import json

def read_json():
    print(f"________ MODULE: read_config.py ___________")

    with open('config.json', 'r') as f:
        configs = json.load(f)

    print(f"read_json(): returning 'config.json' as a dictionary")
    return configs

if __name__ == '__main__':
    read_json()
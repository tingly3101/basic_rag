import yaml



def load_config_yaml(path):
    try:
        with open(path, "r") as yamlfile:
            config = yaml.load(yamlfile, Loader=yaml.FullLoader)
        print(f"Info: loaded {path} successfully.")
        return config
    except FileNotFoundError as e:
        print(f"Error: {path} not found.")
        return False
    
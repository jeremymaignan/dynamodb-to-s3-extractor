import yaml
import os

def get_conf(key):
    try:
        return os.environ[key.upper()]
    except:
        with open('config.yaml') as json_data_file:
            conf = yaml.load(json_data_file)
            return conf[key]
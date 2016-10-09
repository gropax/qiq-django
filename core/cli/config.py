import os
import yaml


def default_config():
    return {
        'editor': "vi % -c 'startinsert'",
        #'test': 'default config',
    }

def default_config_file():
    return os.path.expanduser('~/.qiq.yaml')

def initialize_config_file(path):
    with open(path, 'w') as f:
        f.write('# Enter configuration here\n')

def read_config_file(path=default_config_file()):
    config = default_config()

    if not os.path.isfile(path):
        initialize_config_file(path)

    config.update(yaml.load(open(path, 'r')))

    return Config(config)

class Config(object):
    def __init__(self, data={}):
        self.data = data
        self.__getitem__ = data.__getitem__

    def __iter__(self):
        return self.data.__iter__()

    def get(self, key, default=None):
        if key in self.data:
            val = self.data[key]
            if isinstance(val, dict):
                return Config(val)
            else:
                return val
        elif default == {}:
            return Config()
        else:
            return default

    def __str__(self):
        return self.data.__str__()

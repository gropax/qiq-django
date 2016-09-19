import os


def default_config():
    return {
        'editor': "vi % -c 'startinsert'",
    }

def default_config_file():
    return os.path.expanduser('~/.qiq')

def initialize_config_file(path):
    with open(path, 'w') as f:
        f.write('# Enter configuration here\n')

def read_config_file(path=default_config_file()):
    config = default_config()

    if not os.path.isfile(path):
        initialize_config_file(path)

    with open(path, 'r') as f:
        for l in f.readlines():
            line = l.strip()
            if line and not line.startswith('#'):
                key, val = line.split('=', 1)
                config[key] = val
    return config

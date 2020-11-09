import yaml

class YamlReader(object):
    def fetchYaml(self, path):
        with open(path, 'r') as config:
            return yaml.safe_load(config)
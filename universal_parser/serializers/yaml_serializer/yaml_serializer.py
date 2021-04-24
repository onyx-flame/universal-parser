import yaml
from universal_parser.object_converter import refactor_object, restore_object


class YamlSerializer:
    def dumps(self, obj):
        return yaml.dump(refactor_object(obj))

    def dump(self, obj, fp): # pragma: no cover
        with open(fp, 'w') as outfile:
            yaml.dump(refactor_object(obj), outfile)

    def loads(self, obj):
        return restore_object(yaml.load(obj, Loader=yaml.FullLoader))

    def load(self, fp): # pragma: no cover
        with open(fp, 'r') as outfile:
            return restore_object(yaml.load(outfile.read(), Loader=yaml.FullLoader))


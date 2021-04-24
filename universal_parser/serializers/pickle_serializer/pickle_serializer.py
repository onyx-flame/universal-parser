import pickle
from universal_parser.object_converter import refactor_object, restore_object


class PickleSerializer:
    def dump(self, obj, fp): # pragma: no cover
        with open(fp, 'wb') as outfile:
            pickle.dump(refactor_object(obj), outfile)

    def dumps(self, obj):
        return pickle.dumps(refactor_object(obj))

    def loads(self, s):
        return restore_object(pickle.loads(s))

    def load(self, fp): # pragma: no cover
        with open(fp, 'rb') as outfile:
            return restore_object(pickle.load(outfile))

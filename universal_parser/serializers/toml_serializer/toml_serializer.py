import copy

import pytomlpp as toml
from universal_parser.object_converter import refactor_object, restore_object

class TomlSerializer:
    def dump(self, obj, fp): # pragma: no cover
        ready_obj = TomlSerializer.restructure_primitives(refactor_object(obj))
        with open(fp, 'w') as outfile:
            toml.dump(ready_obj, outfile)

    def dumps(self, obj):
        refactor_object(obj)
        ready_obj = TomlSerializer.restructure_primitives(refactor_object(obj))
        return toml.dumps(ready_obj)

    def loads(self, s):
        new_obj = TomlSerializer.unpack_raw_object(toml.loads(s))
        TomlSerializer.restore_none_values(new_obj)
        return restore_object(new_obj)

    def load(self, fp): # pragma: no cover
        with open(fp, 'r') as outfile:
            return self.loads(outfile.read())

    @staticmethod
    def restructure_primitives(obj):
        restructured_obj = {}
        obj_type = TomlSerializer.get_object_type(obj)
        if type(obj) in (int, float, bool, str, list):
            restructured_obj['type'] = obj_type
            restructured_obj[obj_type] = obj
        elif type(obj) is type(None):
            restructured_obj['type'] = obj_type
        elif type(obj) is dict:
            keys_types = {str(i): TomlSerializer.get_object_type(i) for i in obj}
            restructured_obj['keys_types'] = keys_types
            restructured_obj['type'] = obj_type
            restructured_obj[obj_type] = {str(key): obj[key] for key in obj}
        TomlSerializer.fix_none_values(restructured_obj)
        return restructured_obj

    @staticmethod
    def replace_none_value(obj):
        obj = copy.copy(obj)
        if type(obj) in (int, float, bool, str):
            return obj
        elif type(obj) is type(None):
            return TomlSerializer.restructure_primitives(obj)
        elif type(obj) is list:
            for i in range(len(obj)):
                obj[i] = TomlSerializer.replace_none_value(obj[i])
        elif type(obj) is dict:
            for i in obj:
                obj[i] = TomlSerializer.replace_none_value(obj[i])
        return obj

    @staticmethod
    def fix_none_values(obj):
        if obj.get('type') == 'list':
            my_list = obj['list']
            for i in range(len(my_list)):
                obj['list'][i] = TomlSerializer.replace_none_value(obj['list'][i])
        elif obj.get('type') == 'dict':
            my_dict = obj['dict']
            for i in my_dict:
                my_dict[i] = TomlSerializer.replace_none_value(my_dict[i])

    @staticmethod
    def get_object_type(obj):
        if type(obj) is int:
            return 'int'
        elif type(obj) is float:
            return 'float'
        elif type(obj) is bool:
            return 'bool'
        elif type(obj) is str:
            return 'str'
        elif type(obj) is type(None):
            return 'None'
        elif type(obj) is list:
            return 'list'
        elif type(obj) is dict:
            return 'dict'

    @staticmethod
    def unpack_raw_object(obj):
        obj_type = obj.get('type')
        if obj_type in ('int', 'float', 'bool', 'str', 'list'):
            return obj[obj_type]
        elif obj_type == 'None':
            return None
        elif obj_type == 'dict':
            keys_types = obj['keys_types']
            new_dict = {}
            raw_dict = obj[obj_type]
            for old_key in raw_dict:
                new_key = TomlSerializer.convert_string(old_key, keys_types[old_key])
                new_dict[new_key] = raw_dict[old_key]
            return new_dict

    @staticmethod
    def convert_string(string, obj_type):
        if obj_type == 'int':
            return int(string)
        elif obj_type == 'float':
            return float(string)
        elif obj_type == 'bool':
            return bool(string)
        elif obj_type == 'str':
            return string
        elif obj_type == 'None':
            return None
        elif obj_type == 'list':
            return list(obj_type)
        elif obj_type == 'dict':
            return dict(obj_type)

    @staticmethod
    def restore_none_values(obj):
        if type(obj) is list:
            for i in range(len(obj)):
                if obj[i] == {'type': 'None'}:
                    obj[i] = None
                elif type(obj) in (list, dict):
                    TomlSerializer.restore_none_values(obj[i])
        elif type(obj) is dict:
            for i in obj:
                if obj[i] == {'type': 'None'}:
                    obj[i] = None
                elif type(obj) in (list, dict):
                    TomlSerializer.restore_none_values(obj[i])

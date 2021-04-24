from universal_parser.object_converter import refactor_object, restore_object


class JsonSerializer:
    def dump(self, obj, fp): # pragma: no cover
        with open(fp, 'w') as outfile:
            outfile.write(JsonSerializer.obj_to_json(obj))

    def dumps(self, obj):
        return JsonSerializer.obj_to_json(obj)

    def load(self, fp): # pragma: no cover
        with open(fp, "r") as infile:
            content = infile.read()
        return JsonSerializer.json_to_obj(content)

    def loads(self, s):
        return JsonSerializer.json_to_obj(s)

    @staticmethod
    def obj_to_json(obj):
        ref_obj = refactor_object(obj)
        if type(ref_obj) is int:
            return JsonSerializer.int_to_json(ref_obj)
        elif type(ref_obj) is float:
            return JsonSerializer.float_to_json(ref_obj)
        elif type(ref_obj) is bool:
            return JsonSerializer.bool_to_json(ref_obj)
        elif type(ref_obj) is str:
            return JsonSerializer.str_to_json(ref_obj)
        elif type(ref_obj) is type(None):
            return JsonSerializer.none_to_json(ref_obj)
        elif type(ref_obj) is list:
            return JsonSerializer.list_to_json(ref_obj)
        elif type(ref_obj) is dict:
            return JsonSerializer.dict_to_json(ref_obj)
        else:
            raise ValueError(f"{type(ref_obj)} isn't supported")

    @staticmethod
    def json_to_obj(json_str):
        null = None
        true = True
        false = False
        obj = eval(json_str)
        return restore_object(obj)

    @staticmethod
    def int_to_json(obj):
        return str(obj)

    @staticmethod
    def float_to_json(obj):
        return str(obj)

    @staticmethod
    def bool_to_json(obj):
        return str(obj).lower()

    @staticmethod
    def str_to_json(obj):
        obj = obj.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{obj}"'

    @staticmethod
    def none_to_json(obj):
        return 'null'

    @staticmethod
    def list_to_json(obj):
        result_str = ''
        for item in obj:
            refactored_item = ''
            if type(item) is int:
                refactored_item += JsonSerializer.int_to_json(item)
            elif type(item) is float:
                refactored_item += JsonSerializer.float_to_json(item)
            elif type(item) is bool:
                refactored_item += JsonSerializer.bool_to_json(item)
            elif type(item) is str:
                refactored_item += JsonSerializer.str_to_json(item)
            elif type(item) is type(None):
                refactored_item += JsonSerializer.none_to_json(item)
            elif type(item) in (list, tuple):
                refactored_item += JsonSerializer.list_to_json(item)
            elif type(item) is dict:
                refactored_item += JsonSerializer.dict_to_json(item)
            else:
                raise ValueError(f"{type(item)} isn't supported")
            result_str += refactored_item + ", "
        return '[' + result_str[:-2] + ']'

    @staticmethod
    def dict_to_json(obj):
        result_str = ''
        for key, value in obj.items():
            refactored_item = f'{JsonSerializer.str_to_json(str(key))}: '
            if type(value) is int:
                refactored_item += JsonSerializer.int_to_json(obj[key])
            elif type(value) is float:
                refactored_item += JsonSerializer.float_to_json(obj[key])
            elif type(value) is bool:
                refactored_item += JsonSerializer.bool_to_json(obj[key])
            elif type(value) is str:
                refactored_item += JsonSerializer.str_to_json(obj[key])
            elif type(value) is type(None):
                refactored_item += JsonSerializer.none_to_json(obj[key])
            elif type(value) in (list, tuple):
                refactored_item += JsonSerializer.list_to_json(obj[key])
            elif type(value) is dict:
                refactored_item += JsonSerializer.dict_to_json(obj[key])
            else:
                raise ValueError(f"{type(value)} isn't supported")
            result_str += refactored_item + ", "
        return '{' + result_str[:-2] + '}'

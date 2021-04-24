from universal_parser.serializers.json_serializer.json_serializer import JsonSerializer
from universal_parser.serializers.yaml_serializer.yaml_serializer import YamlSerializer
from universal_parser.serializers.toml_serializer.toml_serializer import TomlSerializer
from universal_parser.serializers.pickle_serializer.pickle_serializer import PickleSerializer


class SerializerFactory:
    def __init__(self):
        self.serializers = {}
        self.register_format('JSON', JsonSerializer)
        self.register_format('YAML', YamlSerializer)
        self.register_format('TOML', TomlSerializer)
        self.register_format('PICKLE', PickleSerializer)

    def register_format(self, format, serializer):
        if format.lower() in self.serializers:
            raise LookupError(f"{format} serializer already exists")
        self.serializers[format.lower()] = serializer

    def get_serializer(self, format):
        serializer = self.serializers.get(format.lower())
        if not serializer:
            raise ValueError(f"{format} format isn't supported")
        return serializer()

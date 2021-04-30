'''import argparse
import configparser
from universal_parser.serializer_factory import SerializerFactory
from universal_parser.logger.logger import get_logger
logger = get_logger(__name__)

def parse(old_format, new_format, file_name):
    factory = SerializerFactory()
    old_format_parser = factory.get_serializer(old_format)
    new_format_parser = factory.get_serializer(new_format)
    intermediate_data = old_format_parser.load(file_name)
    new_format_parser.dump(intermediate_data, file_name.rsplit('.', 1)[0]+'.'+new_format.lower())
    logger.info(f"{file_name} was successfully converted into {file_name.rsplit('.', 1)[0]+'.'+new_format.lower()}")

try:
    parser = argparse.ArgumentParser(description='JSON/TOML/YAML/PICKLE Serializer')
    parser.add_argument('-config', '--config_file', type=str, help='configuration file with settings, primary used')
    parser.add_argument('-old', '--old_format', type=str, help="old format, format of your current file")
    parser.add_argument('-new', '--new_format', type=str, help="new format, format of your future file")
    parser.add_argument('-file', '--file_path', type=str, help="path to your file")
    args = parser.parse_args()
    if args.config_file is not None:
        config = configparser.ConfigParser()
        config.read(args.config_file)
        old_format = config['Serializer']['old_format']
        new_format = config['Serializer']['new_format']
        file_path = config['Serializer']['file_path']
    else:
        old_format = args.old_format
        new_format = args.new_format
        file_path = args.file_path
    if None in (old_format, new_format, file_path):
        raise ValueError('Some arguments left unfilled')
    parse(old_format, new_format, file_path)
except Exception as error:
    logger.error(error, exc_info=True)'''

import configparser
import inspect
import types

from universal_parser.serializer_factory import SerializerFactory
import universal_parser.student as peepo
from universal_parser.object_converter import refactor_object, restore_object, class_to_dict, dict_to_class



factory = SerializerFactory()
parser = factory.get_serializer('json')
print(peepo.Student.__module__)

obj = peepo.Student

dic = {'type': 'class', 'attributes': {}}
if inspect.isclass(obj):

    print('\n')
    for attribute in dir(obj):

        if not attribute.startswith('__') or attribute == '__init__':
            value = getattr(obj, attribute)
        else:
            continue
        dic['attributes'][attribute] = refactor_object(value)

#dic_js = parser.dumps(dic)

st = type("Stud",
          (object, ),
          {})

print(st)

s = peepo.Student(1, 'Kostya', 'Tolok', 4)
#k = st(1, 'Kostya', 'Tolok', 4)
# print(k.sayHello())

print(st)
#k.hello()
#s.hello()

'''print(123432, [i for i in dir(Student) if callable(getattr(Student, i))])
print(dir(Student))
'''
def trash():
    return 1


print(parser.dumps(class_to_dict(peepo.Student)))
print(dict_to_class(class_to_dict(peepo.Student)))


stud_revive = parser.loads(parser.dumps(peepo.Student))
#stud_revive.hello()

vals = {1: peepo.Student(1, 'Kostya', 'Tolok', 4), 2: {3 : {4: peepo.Student(1, 'Kostya', 'Tolok', 4)}}, 5: peepo.Student(1, 'Kostya', 'Tolok', 4)}
print(vals)
print(parser.loads(parser.dumps(vals)))

print(parser.loads(parser.dumps(peepo.MyTest)))
k = types.SimpleNamespace(name='Mike', age=25, gender='male', hfs=trash)
print(vars(k))
print(parser.loads(parser.dumps(peepo.Student)))

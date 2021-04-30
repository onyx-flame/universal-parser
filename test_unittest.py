import unittest
from universal_parser.serializer_factory import SerializerFactory
from universal_parser.student import *
from universal_parser.object_converter import get_function_code_attributes
import numpy

factory = SerializerFactory()


def function1(a):
    return a ** 2


x = 10


def function2(a, b):
    global x
    x += 1
    return a + b * x


def function3(k):
    print(numpy.eye(k))


def function4(name, surname):
    print(f"Hello, {name} {surname}")


class TestJson(unittest.TestCase):
    parser = factory.get_serializer('json')
    serializer = 'json'

    def test_primitives(self):
        some_int = 11
        some_float = 132.345
        some_bool = True
        some_string = 'hel"lo'
        some_none = None
        self.assertEqual(self.parser.loads(self.parser.dumps(some_int)), some_int)
        self.assertEqual(self.parser.loads(self.parser.dumps(some_float)), some_float)
        self.assertEqual(self.parser.loads(self.parser.dumps(some_bool)), some_bool)
        self.assertEqual(self.parser.loads(self.parser.dumps(some_string)), some_string)
        self.assertEqual(self.parser.loads(self.parser.dumps(some_none)), some_none)

    def test_simple_lists_and_tuples(self):
        list1 = [1, 2, 3, 4, 5]
        list2 = [1, '2', 3, '4', 5]
        list3 = [None, 1, '2, 3', False, 98.04]
        tuple1 = (1, 4, 'format', 80, 'json')
        tuple2 = (None, None, 'temp', True, 'rocks')
        tuple3 = ()
        self.assertEqual(self.parser.loads(self.parser.dumps(list1)), list1)
        self.assertEqual(self.parser.loads(self.parser.dumps(list2)), list2)
        self.assertEqual(self.parser.loads(self.parser.dumps(list3)), list3)
        self.assertEqual(tuple(self.parser.loads(self.parser.dumps(tuple1))), tuple1)
        self.assertEqual(tuple(self.parser.loads(self.parser.dumps(tuple2))), tuple2)
        self.assertEqual(tuple(self.parser.loads(self.parser.dumps(tuple3))), tuple3)

    def test_simple_dictionaries(self):
        dict1 = {}
        dict2 = {'1': 'Mon', '2': 'Tue', '3': 'Wed', '4': 'Thu', '5': 'Fri', '6': 'Sat', '7': 'Sun'}
        dict3 = {'Pi': 3.1415, 'Exp': 1.71}
        dict4 = {'Table1': [1, 2, 4], 'Table2': [8, -2, 2.33]}
        self.assertEqual(self.parser.loads(self.parser.dumps(dict1)), dict1)
        self.assertEqual(self.parser.loads(self.parser.dumps(dict2)), dict2)
        self.assertEqual(self.parser.loads(self.parser.dumps(dict3)), dict3)
        self.assertEqual(self.parser.loads(self.parser.dumps(dict4)), dict4)

    def test_functions(self):
        self.assertEqual(self.parser.loads(self.parser.dumps(function1))(123), function1(123))
        self.assertEqual(get_function_code_attributes(self.parser.loads(self.parser.dumps(function1))),
                         get_function_code_attributes(function1))

        self.assertEqual(self.parser.loads(self.parser.dumps(function2))(4, 6), function2(4, 6))
        self.assertEqual(get_function_code_attributes(self.parser.loads(self.parser.dumps(function2))),
                         get_function_code_attributes(function2))

        self.assertEqual(self.parser.loads(self.parser.dumps(function3))(2), function3(2))
        self.assertEqual(get_function_code_attributes(self.parser.loads(self.parser.dumps(function3))),
                         get_function_code_attributes(function3))

        self.assertEqual(self.parser.loads(self.parser.dumps(function4))('name', 'surname'),
                         function4('name', 'surname'))
        self.assertEqual(get_function_code_attributes(self.parser.loads(self.parser.dumps(function4))),
                         get_function_code_attributes(function4))

    def test_classes(self):
        class1 = Student
        class1_instance = Student(95350152, "Daniil", "Trukhan", 953506)
        class2 = MyTest
        class2_instance = MyTest()
        restored_class1 = self.parser.loads(self.parser.dumps(class1))
        restored_class1_instance = restored_class1(95350152, "Daniil", "Trukhan", 953506)
        restored_class2 = self.parser.loads(self.parser.dumps(class2))
        restored_class2_instance = restored_class2()
        self.assertEqual(vars(class1_instance), vars(restored_class1_instance))
        self.assertEqual(class1_instance.hello(), restored_class1_instance.hello())
        self.assertEqual(class1_instance.pp(), restored_class1_instance.pp())
        self.assertEqual(vars(class2_instance), vars(restored_class2_instance))
        self.assertEqual(class1_instance.hello(), restored_class1_instance.hello())

    def test_class_instances(self):
        class_instance1 = Student(95350149, "Konstantin", "Tolok", 953506)
        class_instance2 = MyTest()
        restored_class_instance1 = self.parser.loads(self.parser.dumps(class_instance1))
        restored_class_instance2 = self.parser.loads(self.parser.dumps(class_instance2))
        self.assertEqual(class_instance1.student_id, restored_class_instance1.student_id)
        self.assertEqual(class_instance1.name, restored_class_instance1.name)
        self.assertEqual(class_instance1.surname, restored_class_instance1.surname)
        self.assertEqual(class_instance1.group, restored_class_instance1.group)
        self.assertEqual(class_instance1.pp(), restored_class_instance1.pp())
        self.assertEqual(class_instance1.hello(), restored_class_instance1.hello())
        self.assertEqual(class_instance2.const, restored_class_instance2.const)
        self.assertEqual(class_instance2.hello(), restored_class_instance2.hello())

    def test_complex_lists_and_dictionaries(self):
        structured_object1 = ['value', True, ['1', '2', '3'], {'string': ['my_object', None, 3.14, 21232]}]
        structured_object2 = {'some_value': True, "name": "Daniil", "surname": "Trukhan", "group": 953506,
                              "wave": {"type": "function1",
                                       "source": [1, 0, 0, 1, 2, 67, "7c00640113005300", [None, 2], [], ["x"],
                                                  "C:/Users/Xiaomi/PycharmProjects/lab2_draft/main.py", "sq", 140, "0001"],
                                       "globals": {"__builtins__": "<module \'builtins\' (built-in)>"}}}
        structured_object3 = {"scans": [{"status": None, "starttime": "20150803T000000", "id": 45},
                                        {"status": "completed", "starttime": 15, "id": 539}], "art": "func"}
        structured_object4 = [function1, 'student1', (1, 2, 3, "string")]
        structured_object5 = {"some_func": function1}
        structured_object6 = {'1': function1, '2': {'3': {'4': Student}}, '5': MyTest()}
        self.assertEqual(self.parser.loads(self.parser.dumps(structured_object1)), structured_object1)
        self.assertEqual(self.parser.loads(self.parser.dumps(structured_object2)), structured_object2)
        self.assertEqual(self.parser.loads(self.parser.dumps(structured_object3)), structured_object3)
        self.assertEqual(self.parser.loads(self.parser.dumps(structured_object4))[0](4), 16)
        self.assertEqual(tuple(self.parser.loads(self.parser.dumps(structured_object4))[2]), structured_object4[2])
        self.assertEqual(self.parser.loads(self.parser.dumps(structured_object5)).get('some_func')(2), function1(2))
        restored_structured_object6 = self.parser.loads(self.parser.dumps(structured_object6))
        self.assertEqual(structured_object6['1'](4), restored_structured_object6['1'](4))
        class_instance1 = structured_object6['2']['3']['4'](95350052, "Vyacheslav", "Zakharchuk", 953506)
        restored_class_instance1 = restored_structured_object6['2']['3']['4'](95350052, "Vyacheslav", "Zakharchuk", 953506)
        self.assertEqual(class_instance1.student_id, restored_class_instance1.student_id)
        self.assertEqual(class_instance1.name, restored_class_instance1.name)
        self.assertEqual(class_instance1.surname, restored_class_instance1.surname)
        self.assertEqual(class_instance1.group, restored_class_instance1.group)
        self.assertEqual(class_instance1.pp(), restored_class_instance1.pp())
        self.assertEqual(class_instance1.hello(), restored_class_instance1.hello())
        self.assertEqual(structured_object6['5'].const, restored_structured_object6['5'].const)
        self.assertEqual(structured_object6['5'].hello(), restored_structured_object6['5'].hello())


class TestToml(TestJson):
    parser = factory.get_serializer('toml')
    serializer = 'toml'


class TestPickle(TestJson):
    parser = factory.get_serializer('pickle')
    serializer = 'pickle'


class TestYaml(TestJson):
    parser = factory.get_serializer('yaml')
    serializer = 'yaml'

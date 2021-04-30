class MyTest:
    const = 34
    def hello(self):
        return 'hello from mytest'


class Student(MyTest):

    def __init__(self, student_id, name, surname, group):
        self.student_id = student_id
        self.name = name
        self.surname = surname
        self.group = group

    def pp(self):
        return [self.student_id, self.surname]


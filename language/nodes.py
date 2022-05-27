class Expression(object):
    pass

class Abstraction(Expression):
    def __init__(self, parameter=None, expression=None, parent=None):
        self.parent = parent
        self.parameter = parameter
        self.expression = expression

class Variable(Expression):
    def __init__(self, parent=None, name=''):
        self.parent = parent
        self.name = name

class Application(Expression):
    def __init__(self, left=None, right=None, parent=None):
        self.parent = parent
        self.left = left
        self.right = right
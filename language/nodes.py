class Expression(object):
    pass

class Abstraction(Expression):
    def __init__(self, parameter=None, expression=None, parent=None):
        self.parent = parent
        self.parameter = parameter
        self.expression = expression

    def __repr__(self):
        return 'λ' + repr(self.parameter) + '.' + repr(self.expression)

class Variable(Expression):
    def __init__(self, parent=None, name=''):
        self.parent = parent
        self.name = str(name)

    def __repr__(self):
        return self.name

class Application(Expression):
    def __init__(self, left=None, right=None, parent=None):
        self.parent = parent
        self.left = left
        self.right = right

    def __repr__(self):
        return '(' + repr(self.left) + ' ' + repr(self.right) + ')'


class Assignment:
    def __init__(self, name=None, expression=None, parent=None):
        self.parent = parent
        self.name = str(name)
        self.expression = expression

    def __repr__(self):
        return 'let ' + str(self.name) + ' = ' + repr(self.expression)
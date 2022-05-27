from ast import Expression
from typing import overload
from multipledispatch import dispatch
from language.alpha import alpha_conversion
from language.nodes import Expression, Abstraction, Application, Variable

reduced = False

def is_reduced():
    return reduced

def set_reduced(val):
    global reduced
    reduced = val

def beta_reduction_abstraction(node: Abstraction):
    abstraction = Abstraction()
    abstraction.parameter = beta_reduction(node.parameter)
    abstraction.expression = beta_reduction(node.expression)
    return abstraction

def beta_reduction_variable(node: Variable):
    variable = Variable()
    variable.name = node.name
    return variable

def beta_reduction_application(node: Application):
    global reduced
    if not reduced and type(node.left) is Abstraction:
        reduced = True
        converted = alpha_conversion(node.left.expression, node.left.parameter, node.right)
        return converted
    else:
        application = Application()
        application.left = beta_reduction(node.left)
        application.right = beta_reduction(node.right)
        return application


def beta_reduction(node):
    if type(node) is Application:
        return beta_reduction_application(node)
    elif type(node) is Variable:
        return beta_reduction_variable(node)
    elif type(node) is Abstraction:
        return beta_reduction_abstraction(node)

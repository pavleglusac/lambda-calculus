from typing import overload
from language.nodes import Abstraction, Application, Variable, Expression
from multipledispatch import dispatch


def free_variables_abstraction(node: Abstraction):
    return free_variables(node.expression) - free_variables(node.parameter)

def free_variables_variable(node: Variable):
    return {node.name}

def free_variables_application(node: Application):
    return (free_variables(node.left) | free_variables(node.right))



def bound_variables_abstraction(node: Abstraction):
    return (bound_variables(node.expression) | node.parameter.name)

def bound_variables_variable(node: Variable):
    return {}

def bound_variables_application(node: Application):
    return (bound_variables(node.left) | bound_variables(node.right))


def free_variables(node):
    if type(node) is Application:
        return free_variables_application(node)
    elif type(node) is Variable:
        return free_variables_variable(node)
    elif type(node) is Abstraction:
        return free_variables_abstraction(node)


def bound_variables(node):
    if type(node) is Application:
        return bound_variables_application(node)
    elif type(node) is Variable:
        return bound_variables_variable(node)
    elif type(node) is Abstraction:
        return bound_variables_abstraction(node)
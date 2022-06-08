from ast import Expression
from typing import overload
from language.alpha import alpha_conversion
from language.nodes import Expression, Abstraction, Application, Variable
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from language.predefined import predefined_expressions

reduced = False

lambda_meta = metamodel_from_file('./language/lambda.tx', classes=[Expression, Abstraction, Application, Variable])


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
    if node.name in predefined_expressions:
        return beta_reduction(lambda_meta.model_from_str(predefined_expressions[node.name]))
    return variable

def beta_reduction_application(node: Application):
    global reduced

    if type(node.left) is Variable:
       node.left = beta_reduction(node.left)

    if not reduced and type(node.left) is Abstraction:
        reduced = True
        if type(node.right) is Variable:
            converted = alpha_conversion(node.left.expression, node.left.parameter, beta_reduction_variable(node.right))
        else:
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

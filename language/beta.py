from ast import Expression
from typing import overload
from language.alpha import alpha_conversion
from language.nodes import Expression, Abstraction, Application, Variable
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from language.predefined import named_expressions

applied = False

lambda_meta = metamodel_from_file('./language/lambda.tx', classes=[Expression, Abstraction, Application, Variable])


def was_applied():
    return applied

def set_applied(val):
    global applied
    applied = val

def beta_reduction_abstraction(node: Abstraction):
    abstraction = Abstraction()
    abstraction.parameter = beta_reduction(node.parameter)
    abstraction.expression = beta_reduction(node.expression)
    return abstraction

def beta_reduction_variable(node: Variable):
    variable = Variable()
    variable.name = node.name
    if node.name in named_expressions:
        named_expression_str = named_expressions[node.name]
        named_expression = lambda_meta.model_from_str(named_expression_str)
        return beta_reduction(named_expression)
    return variable

def beta_reduction_application(node: Application):
    global applied

    if type(node.left) is Variable:
       node.left = beta_reduction(node.left)

    if not applied and type(node.left) is Abstraction:
        applied = True
        if type(node.right) is Variable:
            reduced_variable = beta_reduction_variable(node.right)
            converted = alpha_conversion(node.left.expression, node.left.parameter, reduced_variable)
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

from typing import overload
from language.variables import free_variables
from language.nodes import Abstraction, Application, Variable, Expression

def alpha_conversion_abstraction(node: Abstraction, to_convert, converted):
    abstraction = Abstraction()
    if node.parameter.name in free_variables(converted):
        changed_name = "afnjsdajfalj"
        changed_parameter = Variable()
        changed_name.name = changed_name
        abstraction.parameter = changed_parameter
        abstraction.expression = alpha_conversion(node.expression, node.parameter, changed_parameter)
    else:   
        abstraction.parameter = alpha_conversion(node.parameter, to_convert, converted)
        abstraction.expression = alpha_conversion(node.expression, to_convert, converted)
    return abstraction

def alpha_conversion_variable(node: Variable, to_convert, converted):
    if node.name == to_convert.name:
        return converted
    variable = Variable()
    variable.name = node.name
    return variable

def alpha_conversion_application(node: Application, to_convert, converted):
    application = Application()
    application.left = alpha_conversion(node.left, to_convert, converted)
    application.right = alpha_conversion(node.right, to_convert, converted)
    return application


def alpha_conversion(node, to_convert, converted):
    if type(node) is Application:
        return alpha_conversion_application(node, to_convert, converted)
    elif type(node) is Variable:
        return alpha_conversion_variable(node, to_convert, converted)
    elif type(node) is Abstraction:
        return alpha_conversion_abstraction(node, to_convert, converted)


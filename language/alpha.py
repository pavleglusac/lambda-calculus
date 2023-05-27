from typing import overload
from language.variables import free_variables, bound_variables
from language.nodes import Abstraction, Application, Variable, Expression
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from language.predefined import named_expressions


unavailable_names = set()

lambda_meta = metamodel_from_file('./language/lambda.tx', classes=[Expression, Abstraction, Application, Variable])

def alpha_conversion_abstraction(node: Abstraction, to_convert, converted):
    global unavailable_names
    abstraction = Abstraction()
    print("ALPHA CONVERSION ABSTRACTION")
    print(node.parameter, node.expression, to_convert, converted)
    unavailable_names = unavailable_names | free_variables(converted) | bound_variables(converted)
    if node.parameter.name in unavailable_names:
        changed_name = generate_next_variable_name(unavailable_names | {node.parameter.name})
        changed_parameter = Variable()
        changed_parameter.name = changed_name
        abstraction.parameter = changed_parameter
        unavailable_names.add(changed_name)
        new_expr = alpha_conversion(node.expression, node.parameter, changed_parameter)
        #new_expr = alpha_conversion(new_expr, to_convert, converted)
        abstraction.expression = alpha_conversion(new_expr, to_convert, converted)
        print(abstraction)
    else:   
        abstraction.parameter = alpha_conversion(node.parameter, to_convert, converted)
        abstraction.expression = alpha_conversion(node.expression, to_convert, converted)
        print("ay ", abstraction)
    return abstraction

def alpha_conversion_variable(node: Variable, to_convert, converted):
    # print("ALPHA CONVERSION VARIABLE")
    if type(to_convert) is Variable:
        if node.name == to_convert.name:
            return converted
    variable = Variable()
    variable.name = node.name
    return variable

def alpha_conversion_application(node: Application, to_convert, converted):
    # print("ALPHA CONVERSION APPLICATION")
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

def generate_next_variable_name(unavailable_names):
    word = "a"
    MAXIMUM_NAMES_LIMIT = 10_000_000
    for _ in range(MAXIMUM_NAMES_LIMIT):
        if word in unavailable_names:
            word = nextWord(word)
        else:
            return word

def nextWord(s):
    if s == " ":
        return "a"    
    ind = next((i for i, c in enumerate(s) if c != 'z'), -1)
    if ind == -1:
        s += 'a'
    else:
        s = s[:ind] + chr(ord(s[ind]) + 1) + s[ind+1:]
    return s

def clear_unavailable():
    global unavailable_names
    unavailable_names.clear()


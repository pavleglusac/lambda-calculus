# Expression  -> Variable | Application | Abstraction
# Variable    -> ID
# Application -> (Expression Expression)
# Abstraction -> λID.Expression
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from language.nodes import Expression, Abstraction, Application, Variable
from language.alpha import alpha_conversion, clear_unavailable
from language.beta import beta_reduction, was_applied, set_applied
from language.predefined import named_expressions
from language.nodes import Expression, Abstraction, Application, Variable, Assignment

import pydot_ng as pydot
import os

lambda_meta = metamodel_from_file('./language/lambda.tx', classes=[Expression, Abstraction, Application, Variable, Assignment])
metamodel_export(lambda_meta, 'metamodel.dot')
graph = pydot.graph_from_dot_file('metamodel.dot')
graph.write_svg('./static/metamodel.svg')

MAX_ITERATIONS = 100

def print_tree(model):
    print(model_to_string(model))

def model_to_string(model):
    if type(model) is Abstraction:
        return 'λ' + model_to_string(model.parameter) + '.' + model_to_string(model.expression)
    elif type(model) is Application:
        return '(' + model_to_string(model.left) + ' ' + model_to_string(model.right) + ')'
    elif type(model) is Variable:
        return str(model.name)


def interpret(value, user):
    try:
        input_model = get_model_from_value(value)
        return handle_model(input_model, user)
    except Exception as e:
        log_exception(e)
        raise e


def get_model_from_value(value):
    input_model = lambda_meta.model_from_str(value)
    model_export(input_model, 'model.dot')
    return input_model


def handle_model(input_model, user):
    if type(input_model) is Assignment:
        return add_named_expression(input_model)
    else:
        return perform_reduction(input_model, user)


def add_named_expression(input_model):
    named_expressions[input_model.name] = repr(input_model.expression)
    return [f'Added {input_model.name} = {repr(input_model.expression)}']


def perform_reduction(input_model, user):
    i = 0
    applied = True
    evaluation_steps = []
    print(type(input_model))
    clear_unavailable()
    while applied and i < MAX_ITERATIONS:
        evaluation_steps.append(model_to_string(input_model))
        input_model = beta_reduce_and_save(input_model, i, user)
        applied = was_applied()
        set_applied(False)
        i += 1
    return evaluation_steps


def beta_reduce_and_save(input_model, iteration, user):
    beta_reduced_model = beta_reduction(input_model)
    save_model(f'model{iteration}', input_model, user)
    return beta_reduced_model


def log_exception(e):
    print(e)
    import traceback
    traceback.print_exc()


def save_model(path, model, user):
    model_export(model, './language/models/'+path+'.dot')
    graph = pydot.graph_from_dot_file('./language/models/'+path+'.dot')
    isExist = os.path.exists('./static/'+user)
    if not isExist:
        os.makedirs('./static/'+user)
    graph.write_svg('./static/'+user+'/'+path+'.svg')


if __name__ == '__main__':
    pass
    # interpret('(λm.((m λt.λf.t) λx.λt.λf.f) λz.λs.z)')

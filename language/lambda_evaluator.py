# Expression  -> Variable | Application | Abstraction
# Variable    -> ID
# Application -> (Expression Expression)
# Abstraction -> λID.Expression
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from language.nodes import Expression, Abstraction, Application, Variable
from language.alpha import alpha_conversion, unavailable_names
from language.beta import beta_reduction, is_reduced, set_reduced
import pydot_ng as pydot
import os

lambda_meta = metamodel_from_file('./language/lambda.tx', classes=[Expression, Abstraction, Application, Variable])
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
        return model.name


def interpret(value, user):
    try:
        input_model = lambda_meta.model_from_str(value)
        model_export(input_model, 'model.dot')
        print_tree(input_model)
        print()
        print("-"*25, end='\n\n')
        print()
        i = 0
        reduced = False
        evaluation_steps = []
        while not reduced and i < MAX_ITERATIONS:
            evaluation_steps.append(model_to_string(input_model))
            nesto = beta_reduction(input_model)
            save_model('model'+str(i), input_model, user)
            print_tree(input_model)
            print()
            print("-"*25, end='\n\n')
            print_tree(nesto)
            input_model = nesto
            print()
            unavailable_names.clear()
            reduced = not is_reduced()
            set_reduced(False)
            i += 1
        return evaluation_steps
    except Exception as e:
        print(e)
        raise e

def save_model(path, model, user):
    model_export(model, './language/models/'+path+'.dot')
    graph = pydot.graph_from_dot_file('./language/models/'+path+'.dot')
    isExist = os.path.exists('./static/'+user)
    if not isExist:
        os.makedirs('./static/'+user)
    graph.write_svg('./static/'+user+'/'+path+'.svg')


if __name__ == '__main__':
    interpret('(λm.((m λt.λf.t) λx.λt.λf.f) λz.λs.z)')

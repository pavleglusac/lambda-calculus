# Expression  -> Variable | Application | Abstraction
# Variable    -> ID
# Application -> (Expression Expression)
# Abstraction -> λID.Expression
import imp
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from language.nodes import Expression, Abstraction, Application, Variable
from language.alpha import alpha_conversion
from language.beta import beta_reduction, is_reduced, set_reduced
import pydot

lambda_meta = metamodel_from_file('./language/lambda.tx', classes=[Expression, Abstraction, Application, Variable])
metamodel_export(lambda_meta, 'metamodel.dot')

MAX_ITERATIONS = 100

def print_tree(model):
    print(model_to_string(model))

def model_to_string(model):
    if type(model) is Abstraction:
        return '(λ' + model.parameter.name + '.' + model_to_string(model.expression) + ')'
    elif type(model) is Application:
        return '(' + model_to_string(model.left) + ' ' + model_to_string(model.right) + ')'
    elif type(model) is Variable:
        return model.name


def interpret(value):
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
            save_model('model'+str(i), input_model)
            print_tree(input_model)
            print()
            print("-"*25, end='\n\n')
            print_tree(nesto)
            input_model = nesto
            print()
            reduced = not is_reduced()
            set_reduced(False)
            i += 1
        return evaluation_steps
    except Exception as e:
        e.with_traceback()
        print(e)

def save_model(path, model):
    model_export(model, './language/models/'+path+'.dot')
    graphs = pydot.graph_from_dot_file('./language/models/'+path+'.dot')
    graph = graphs[0]
    graph.write_svg('./static/'+path+'.svg')


if __name__ == '__main__':
    interpret('(λm.((m λt.λf.t) λx.λt.λf.f) λz.λs.z)')

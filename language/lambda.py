# Expression  -> Variable | Application | Abstraction
# Variable    -> ID
# Application -> (Expression Expression)
# Abstraction -> λID.Expression
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from nodes import Expression, Abstraction, Application, Variable
from alpha import alpha_conversion
from beta import beta_reduction, isreduced

lambda_meta = metamodel_from_file('lambda.tx', classes=[Expression, Abstraction, Application, Variable])
metamodel_export(lambda_meta, 'metamodel.dot')

MAX_ITERATIONS = 100

def print_tree(model):
    print(model)


def interpret(value):
    try:
        input_model = lambda_meta.model_from_str(value)
        model_export(input_model, 'model.dot')
        i = 0
        while not isreduced() and i < MAX_ITERATIONS:
            print("aloo")
            print(input_model)
            beta_reduction(input_model)
            print_tree(input_model)
            i += 1
    except Exception as e:
        print(e)


if __name__ == '__main__':
    interpret('λX.X')

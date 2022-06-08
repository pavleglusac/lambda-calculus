from textx import metamodel_from_file
hello_meta = metamodel_from_file('hello.tx')
hello_model = hello_meta.model_from_str('hello World, Solar System, Universe')
print("Greeting", ", ".join([to_greet.name for to_greet in hello_model.to_greet]))

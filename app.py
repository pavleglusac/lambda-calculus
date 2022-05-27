from flask import Flask, redirect, render_template, request, url_for
from livereload import Server
from language.lambda_evaluator import interpret

app = Flask(__name__)

evaluation = [
    '(λx. t (x x)) (λx. t (x x))',
    't ((λx. t (x x)) (λx. t (x x)))',
    't (Y t) '
]

app.config.update(
    TESTING=True,
    TEMPLATES_AUTO_RELOAD=True
)

@app.route('/index')
@app.route("/")
def index():
    return render_template('index.html', expressions=evaluation)

@app.route("/evaluate", methods=['POST'])
def evaluate():
    global evaluation
    expression = request.form['expression']
    evaluation = interpret(expression)
    return redirect(url_for('index'))


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/examples")
def examples():
    return render_template('examples.html')

    
if __name__ == '__main__':
    app.run()

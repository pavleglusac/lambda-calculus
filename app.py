from flask import Flask, render_template
from livereload import Server

app = Flask(__name__)

sample_evaluation = [
    '(λx. t (x x)) (λx. t (x x))',
    't ((λx. t (x x)) (λx. t (x x)))',
    't (Y t) '
]

app.config.update(
    TESTING=True,
    TEMPLATES_AUTO_RELOAD=True
)

@app.route("/")
def index():
    return render_template('index.html', expressions=sample_evaluation)

@app.route("/about")
def about():
    return render_template('about.html')

    
if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.serve()


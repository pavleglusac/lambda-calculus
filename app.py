import os.path

from flask import Flask, redirect, render_template, request, url_for, session
from language.lambda_evaluator import interpret
import uuid
import datetime
import shutil
from flask import send_from_directory


app = Flask(__name__)
app.secret_key = 'lambda calculus secret key'
app.debug = True

evaluation = [
    '(λx. t (x x)) (λx. t (x x))',
    't ((λx. t (x x)) (λx. t (x x)))',
    't (Y t) '
]

sessions = {}

app.config.update(
    TESTING=True,
    TEMPLATES_AUTO_RELOAD=True
)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/index')
@app.route("/")
def index():
    make_session()
    return render_template('index.html', expressions=session['eval'], err=session['err'])

def make_session():
    if 'user_id' not in session:
        session['user_id'] = uuid.uuid4().hex
        session['start'] = datetime.datetime.now(datetime.timezone.utc)
        session['eval'] = []
        sessions[session['user_id']] = session
        session['err'] = ''
    else:
        if session['user_id'] not in sessions.keys():
            sessions[session['user_id']] = session
            session['start'] = datetime.datetime.now(datetime.timezone.utc)
            session['eval'] = []
            session['err'] = ''

@app.route("/evaluate", methods=['POST'])
def evaluate():
    make_session()
    expression = request.form['expression']
    try:
        session['eval'] = interpret(expression, session['user_id'])
    except Exception as e:
        session['err'] = str(e)
    return redirect(url_for('index'))


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/examples")
def examples():
    return render_template('examples.html')


@app.before_request
def before_request_callback():
    if request.endpoint == 'evaluate':
        to_remove = []
        for id, ses in sessions.items():
            # print(id)
            # print(ses['start'] - datetime.datetime.now(datetime.timezone.utc))
            # print(datetime.datetime.now(datetime.timezone.utc) - ses['start'])
            # print(datetime.timedelta(seconds=10))
            # print(datetime.datetime.now(datetime.timezone.utc) - ses['start'] > datetime.timedelta(seconds=10))
            # print("*"*50)
            if datetime.datetime.now(datetime.timezone.utc) - ses['start'] > datetime.timedelta(seconds=10):
                # print("to remove", id)
                remove_folder('./static/' + id)
                to_remove.append(id)
        for id in to_remove:
            del sessions[id]

        # print("INTERCEPTED")

def remove_folder(folder):
    if not os.path.exists(folder):
        return
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    os.rmdir(folder)
    
if __name__ == '__main__':
    app.run()

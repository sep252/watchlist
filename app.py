from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'

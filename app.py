from flask import Flask
from markupsafe import escape

app = Flask(__name__)
@app.route('/')
def hello():
    return '<h1>Hello Totoro</h1><img src="http://helloflask.com/totoro.gif">'

# 一个函数可以绑定多个路由
@app.route('/index')
@app.route('/home')
def hello_home():
    return '<h1>HelloHome</h1>'
    
@app.route('/user/<username>')
def hello_user(username):
    return f'<h1>HelloUser: {username}</h1>'

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', username='totoro'))
   
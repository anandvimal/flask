from flask import Flask, request, make_response, redirect, abort
app = Flask(__name__)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response
    #return '<h1>Hello World! your User-Agent is {}</h1>'.format(user_agent)

@app.route('/red')
def red():
    return redirect('http://www.example.com')

def load_user(id):
    if int(id)>10:
        return id
    else:
        return False
    
@app.route('/userid/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello, {}</h1>'.format(user)


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

@app.route('/bad')
def bad_response():
    return '<h1>This is a fail! sending 400', 400
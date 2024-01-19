from flask import Flask, request, make_response, abort, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap

#import app
app = Flask(__name__)

#for flask wtf form
app.config['SECRET_KEY'] = 'hard to guess string' #its non prod env

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#import bootstrap
bootstrap = Bootstrap(app)

#import flask momentjs
from flask_moment import Moment 
moment = Moment(app)
from datetime import datetime

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        #form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/testcommontemplate')
def testcommontemplate():
    return render_template('testcommon.html')

all_comments = ['one','two','three', 'four', 'five']
@app.route('/listcomments')
def allcomments():
    return render_template('comments.html', comments=all_comments)
        

@app.route('/blue')
def blue():
    user_agent = request.headers.get('User-Agent')
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response

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


@app.route('/bad')
def bad_response():
    return '<h1>This is a fail! sending 400', 400

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server(e):
    return render_template('500.html'), 500
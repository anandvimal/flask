from flask import Flask, request, make_response, abort, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap

from dotenv import load_dotenv

#flask sql alchemy requirements
import os
from flask_sqlalchemy import SQLAlchemy

#flask migrate framework
from flask_migrate import Migrate

#load env variables from .env file
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

#import app
app = Flask(__name__)

#sql alchemy config
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#for flask wtf form
app.config['SECRET_KEY'] = 'hard to guess string' #its non prod env

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#bootstrap requirements
bootstrap = Bootstrap(app)

#flask momentjs requirements
from flask_moment import Moment 
moment = Moment(app)
from datetime import datetime


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<Users %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))

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
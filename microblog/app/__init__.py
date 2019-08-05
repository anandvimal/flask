from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

#app.config['SECRET KEY'] = 'you-will-never-guess'
#we can add more variables here as needed

from app import routes

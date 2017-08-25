from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
import config

app = Flask(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='mysql://user:pass@hostname/dbname',
    SECRET_KEY='abcd1234',
    DEBUG=True,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
))
app.config.from_envvar('CONFIG', silent=True)
db = SQLAlchemy(app)

from views import *

db.create_all()

if __name__ == '__main__':
    app.run()

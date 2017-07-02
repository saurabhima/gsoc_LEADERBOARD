from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = 'abc1234'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dbadmin:dbadministrator@localhost/donorworkflow'
db = SQLAlchemy(app)

from views import *

if __name__ == '__main__':
    app.run()

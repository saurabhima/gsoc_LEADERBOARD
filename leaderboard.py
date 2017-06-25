from flask import Flask

app = Flask(__name__)
app.secret_key = 'abc1234'
app.config['DEBUG'] = True
from views import *




if __name__ == '__main__':

    app.run()

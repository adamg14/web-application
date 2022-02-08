from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
app = Flask(__name__)
app.config['SECRET_KEY'] = '83f7cc253f0699b3814f4570669f1f86bcba2c76a59f398f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c2044210:Password2001@csmysql.cs.cf.ac.uk:3306/c2044210_database2'

login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from shop import routes, models
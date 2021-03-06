from flask import Flask
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity)
from flask_bcrypt import Bcrypt
import os, config

app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')

db = SQLAlchemy(app)
ma = Marshmallow(app)
mail = Mail(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


#from . import views
from app import routes, models

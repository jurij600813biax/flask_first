import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '00000000'
#    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    JWT_SECRET_KEY = 'super-secret'
   
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'mobile.service.parko28@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'Rusl@n1988'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    
class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
    'sqlite:///' + os.path.join(app_dir, 'app.db')    

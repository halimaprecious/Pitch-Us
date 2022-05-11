from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_uploads import UploadSet,configure_uploads,IMAGES

bootstrap = Bootstrap()
db =SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()
photos =UploadSet('photos',IMAGES)
# mail = Mail()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

#photo uploads config
app.config['UPLOADED_PHOTOS_DEST'] ='app/static/photos'

# email configurations
# MAIL_SERVER = 'smtp.googlemail.com'
# MAIL_PORT = 587
# MAIL_USE_TLS = True
# MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
# MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

def create_app():
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #initialize extentions
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)
    # mail.init_app(app)

    #configure uploadset
    configure_uploads(app,photos)

    #registering blueprint
    from .views import views
    app.register_blueprint(views,url_prefix="/")

    from .auth import auth
    app.register_blueprint(auth,url_prefix="/")

    from .models import User,Pitch, Comment,Like


    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login" # redirects to login page
    login_manager.init_app(app)

    #access user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists("app/"+DB_NAME):
        db.create_all(app=app)
        print("Created database!")
   
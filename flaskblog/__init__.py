from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flaskblog.config import Config

# Bootstrap for WTForms
bootstrap = Bootstrap5()

# Login manager
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# CKEditor for edit and post forms
ckeditor = CKEditor()

# SQLite database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Bcrypt for password hashing
bcrypt = Bcrypt()

# Mail
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    bootstrap.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
  

    return app

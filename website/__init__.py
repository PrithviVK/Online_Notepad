from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager #used to manage login related things

db=SQLAlchemy()#database object for adding updating and deleting 
DB_NAME ="database.db"

def create_app():
    app=Flask(__name__)
    #  secret key for the app that should be private to you in production stages
    app.config['SECRET_KEY']='Hola!' #can be changed ig
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'#telling flask where database is located basically in website folder
    db.init_app(app)

    login_manager=LoginManager()
    login_manager.login_view='auth.login'# if user is not logged in it should be redirected to auth.login
    login_manager.init_app(app)#  telling login_manager which app is to be used 

    from .views import views
    from .auth import auth
    # import Python.website.models as models
    from . import models
    from .models import User,Note

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    with app.app_context():
        db.create_all()

    @login_manager.user_loader # a decorator to load user
    def load_user(id):#telling flask how we should load a user
        return User.query.get(int(id)) #gets the primary key of User by default


    # create_database(app)

    return app  

# def create_database(app):
#     if not path.exists('website/'+DB_NAME):#if no db then create a new db 
#         db.create_all(app=app)
#         print('Database Created')




   
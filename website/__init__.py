#__init__.py makes this website folder a python package . this means from any python file,we can import website folder thereand after import all thing which are in __init__.py will be in that file . when we import the folder name everthing in __init__.py runs

# initilization stuff for our flask application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_login import LoginManager

db = SQLAlchemy()  
DB_NAME = "database.db"

# flask initilization - create a flask application and return it
def create_app():
    app = Flask(__name__)#__name__ is name of the module that you are going to run to create this app
    app.config["SECRET_KEY"] = "helloworld" #to encrypt session data . in production dont leak this
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app) # initilise our database

    '''
    # we will not use this way . we will store this in a new file name views.py
    # created route/view or endpoints
    @app.route("/")
    def home():
        return "<h1>Hello</h1>"# now at slash in the url we would se hello

    @app.route("/profile")
    def profile():
        return "<h1>Profile</h1>"
    '''
    from .views import views2 # we are using . operator because we are doing a relative import as views file is imported from inside website package
    from .auth import auth2

    app.register_blueprint(views2,url_prefix="/")
    app.register_blueprint(auth2,url_prefix="/")

    from .models import User , Post

    login_manager = LoginManager() # can access certain pages if they are loggedin but can't access some pages if they are not logged in . no need to enter username and password every time to view certain pages
    login_manager.login_view = "auth.login" # if someone tries to access a page and they are not logged in so we will redirect to auth.py -> login route
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    create_database(app)
    return app

def create_database(app):
    if not path.exists("website/"+DB_NAME):
        db.create_all(app=app)
        print("Created database!")



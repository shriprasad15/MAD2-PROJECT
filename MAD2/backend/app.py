import os
from flask import Flask, g, jsonify,render_template, render_template_string,request,redirect,url_for,session
from flask_restful import Resource, Api
from config import Config
from workers import *
from flask_security import SQLAlchemySessionUserDatastore, Security
from flask_cors import CORS
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from apis import Homepage, UserApi, Login, Category, CategoryCRUD, Product_API, ProductCRUD, Cart, CartCRUD, exports, Celery_API
from flask_login import LoginManager

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)
    with app.app_context():
        from models import db, User, Role
        
    login = LoginManager(app)
    db.init_app(app)
    api = Api(app)
    CORS(app)
    # user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role) 
    # app.security = Security(app, user_datastore)
    user_manager = UserManager(app, db, User)
    
    with app.app_context():
        db.create_all()
        if Role.query.count() == 0:
            print("Creating Database")
            
            r1=app.security.datastore.find_or_create_role(name="user")
            r2=app.security.datastore.find_or_create_role(name="manager")
            r3=app.security.datastore.find_or_create_role(name="admin")
            u1=app.security.datastore.create_user( email="admin@gmail.com", password=generate_password_hash("admin"), roles=["admin", "manager", "user"])
            db.session.commit()
        else:
            print("Database already exists")

    api.add_resource(Homepage,'/')
    api.add_resource(UserApi, '/user')

    api.add_resource(Login, '/login_user')

    api.add_resource(Category, '/category') # get and post
    api.add_resource(CategoryCRUD, "/category/<id>")

    api.add_resource(Product_API, '/product/cat/<int:cat_id>')
    api.add_resource(ProductCRUD,'/product/<prod_id>')

    api.add_resource(Cart, '/cart/<user_id>')
    api.add_resource(CartCRUD, '/cart/<id>/<userid>')

    api.add_resource(exports, "/export")
    api.add_resource(Celery_API, "/celery")

    return app,api

app, api = create_app()
# with app.app_context():
    
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
login = LoginManager(app)

@login.user_loader
def load_user(id):
    from models import User
    return User.query.get(int(id))

@app.route('/a')
def home_page():
    return render_template_string("home page")

# The Members page is only accessible to authenticated users
@app.route('/members')
@login_required    # Use of @login_required decorator
def member_page():
    return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>Members page</h2>
                <p><a href={{ url_for('user.register') }}>Register</a></p>
                <p><a href={{ url_for('user.login') }}>Sign in</a></p>
                <p><a href={{ url_for('home_page') }}>Home Page</a> (accessible to anyone)</p>
                <p><a href={{ url_for('member_page') }}>Member Page</a> (login_required: member@example.com / Password1)</p>
                <p><a href={{ url_for('admin_page') }}>Admin Page</a> (role_required: admin@example.com / Password1')</p>
                <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
            {% endblock %}
            """)

    # The Admin page requires an 'Admin' role.
@app.route('/admin')
@roles_required('Admin')    # Use of @roles_required decorator
def admin_page():
    return render_template_string("admin only")

    




def celery_func():
    # cache.init_app(app)

    celery1 = celery
    celery1.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"]
    )
    celery1.Task = ContextTask
    # Setting Flask Security Setup
    app.app_context().push()

    return celery1


celery = celery_func()

from flask import send_file
@app.route('/download_csv')
def download_csv():
    return send_file(f'./instance/name.csv', as_attachment=True)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
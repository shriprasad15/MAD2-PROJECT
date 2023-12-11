import os
from flask import Flask, g, jsonify,render_template, render_template_string,request,redirect,url_for,session
from flask_security import current_user, auth_required, login_required, roles_required, roles_accepted
from flask_restful import Api, Resource, reqparse, fields, marshal_with, marshal
from config import Config
from workers import *
from flask_security import SQLAlchemySessionUserDatastore, Security
from flask_cors import CORS
from database import fun
from sec import datastore, db
from apis import api
from werkzeug.security import check_password_hash, generate_password_hash
from models import Category
from apis import Homepage, UserApi, Login, Category_resource, CategoryCRUD, Product_API, ProductCRUD, Cart, CartCRUD, exports, Celery_API
from flask_login import LoginManager


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)
    with app.app_context():
        from models import User, Role
    api.init_app(app)
    db.init_app(app)
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role) # Not SQLAlchemyUserDatastore
    app.security = Security(app, user_datastore)
    CORS(app)
    
    # app.security = Security(app,datastore)
    
    
    with app.app_context():
        db.create_all()
      
        if Role.query.count() == 0:
            print("Creating Database")
            
            r1=app.security.datastore.find_or_create_role(name="user")
            r2=app.security.datastore.find_or_create_role(name="manager")
            r3=app.security.datastore.find_or_create_role(name="admin")
            u1=app.security.datastore.create_user( email="admin@gmail.com", password=generate_password_hash("password"), roles=["admin", "manager", "user"], fname="admin", lname="admin", mobile=1234567890,username="admin")
            db.session.commit()
        elif Category.query.count() == 0:
            fun()
        else:
            print("Database already exists")

    # api.add_resource(Homepage,'/')
    # api.add_resource(UserApi, '/user')

    # api.add_resource(Login, '/login_user')

    # api.add_resource(Category_resource, '/category') # get and post
    # api.add_resource(CategoryCRUD, "/category/<id>")

    # api.add_resource(Product_API, '/product/cat/<int:cat_id>')
    # api.add_resource(ProductCRUD,'/product/<prod_id>')

    # api.add_resource(Cart, '/cart/<user_id>')
    # api.add_resource(CartCRUD, '/cart/<id>/<userid>')

    # api.add_resource(exports, "/export")
    # api.add_resource(Celery_API, "/celery")

    return app

app= create_app()

    
with app.app_context():
    import views

# @login.user_loader
def load_user(id):
    from models import User
    return User.query.get(int(id))

@app.route('/a')
def home_page():
    return render_template_string("home page")



@app.route('/create-role/<string:role>')
# @login_required('token')
@roles_required('admin')
def create_role(role):

    app.security.datastore.create_role(name=role)
    db.session.commit()

    return "Role Created Successfully"
    
@app.route('/create-user', methods=['POST'])
def create_user():
    from models import User, Role,UserRoles
    data=request.get_json()
    app.security.datastore.create_user(email=data.get('email'), password=generate_password_hash(data.get("password")),roles=data.get('roles'),fname=data.get("fname"),lname=data.get("lname"),mobile=data.get("mobile"),username=data.get("username"))
    db.session.commit()
    email = data.get('email')

    return email


def add_user(email,username,fname,lname,mobile,password,roles):
    app.security.datastore.create_user(email=email,username=username,fname=fname,lname=lname,mobile=mobile,password=password,roles=roles)
    db.session.commit()
    return email


def find_user(email):
    return datastore.find_user(email=email)


login_data= reqparse.RequestParser()

login_data.add_argument('email')
login_data.add_argument('password')
@app.route('/login_user', methods=['POST'])
def logiin(self):
        from models import User
        args=login_data.parse_args()
        email=args["email"]
        password=args['password']
        print(email, password)

        # verify_email and password\
        # to verify password, use check_password_hash
        # to verify email, use User.query.filter_by(email=email).first()

        user = find_user(email)

        print(user.email)
        if not user:
            return jsonify({"message": "User Not Found"}), 404
        if check_password_hash(user.password, password):
            login_user(user)
            print("password matched")
            return jsonify({"token": user.get_auth_token(), "email": user.email, "role": get_user_roles(user.roles)})
        else:
            print("password not matched")
            return jsonify({"message": "Wrong Password"}), 400



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
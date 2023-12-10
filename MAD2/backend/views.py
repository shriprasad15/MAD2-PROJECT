
from flask import current_app as app, jsonify, request, render_template, send_file
from flask_security import auth_required, roles_required
from sec import datastore

from werkzeug.security import generate_password_hash
from models import db
from werkzeug.security import check_password_hash



@app.post('/user-signup')
def user_signup():
    data=request.get_json()
    email = data.get('email')
    fname=data.get('fname')
    lname=data.get('lname')
    mobile=data.get('mobile')
    if not email:
        return jsonify({"message": "email not provided"}), 400

    user = datastore.find_user(email=email)

    if  user:
        return jsonify({"message": "User Already present"}), 403
    else:
        user = datastore.create_user(email=email, password=generate_password_hash(data.get("password")),roles=['user'],fname=fname,lname=lname,mobile=mobile)

        db.session.commit()
        return jsonify({"message": "User Created"}), 200

@app.post('/user-login')
def user_login():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"message": "email not provided"}), 400

    user = datastore.find_user(email=email)

    if not user:
        return jsonify({"message": "User Not Found"}), 404

    if check_password_hash(user.password, data.get("password")):
        return jsonify({"token": user.get_auth_token(), "email": user.email, "role": user.roles[0].name})
    else:
        return jsonify({"message": "Wrong Password"}), 400



@app.get('/admin')
@auth_required("token")
@roles_required("admin")
def admin():
    return "Hello Admin"

print("fromm flask_api.py")
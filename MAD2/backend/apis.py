from flask_restful import Resource, Api, reqparse, fields, marshal_with
from models import *
from flask import request

class Homepage(Resource):
    def get(self):
        return {"hello": "World"}

user_data= reqparse.RequestParser()

user_data.add_argument('fname')
user_data.add_argument('lname')
user_data.add_argument('mobile')
user_data.add_argument('email')
user_data.add_argument('password')

user_fields= {
    'fname': fields.String,
    'lname': fields.String,
    'mobile': fields.Integer,
    'email': fields.String
}

class USERApi(Resource):
    def get(self):
        return {"hello": "User"}

    @marshal_with(user_fields)
    def post(self):
        args=user_data.parse_args()
        print(args)

        user= User(fname=args['fname'], lname= args['lname'], mobile=args['mobile'], email=args['email'])
        session.add(user)
        session.commit()
        return user
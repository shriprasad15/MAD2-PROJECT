from flask import Flask,render_template,request,redirect,url_for,session
from flask_restful import Resource, Api

app = Flask(__name__, template_folder="templates")
from models import *
from apis import *

api = Api(app)
api.add_resource(Homepage,'/')
api.add_resource(USERApi, '/user')
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
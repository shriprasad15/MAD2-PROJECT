from flask import Flask,render_template,request,redirect,url_for,session
from flask_restful import Resource, Api

app = Flask(__name__, template_folder="templates")
from models import *
from apis import *

api = Api(app)
api.add_resource(Homepage,'/')
api.add_resource(UserApi, '/user_signup')

api.add_resource(Category, '/category') # get and post
api.add_resource(CategoryCRUD, "/category/<id>")

api.add_resource(Product, '/product/cat/<int:cat_id>')
api.add_resource(ProductCRUD,'/product/<prod_id>')

api.add_resource(Cart, '/cart/<user_id>')
api.add_resource(CartCRUD, '/cart/<id>/<userid>')

api.add_resource(exports, "/export")
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
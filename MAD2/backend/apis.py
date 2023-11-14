from flask_restful import Resource, Api, marshal, reqparse, fields, marshal_with
from models import *
from flask import request

class Homepage(Resource):
    def get(self):
        return {"hello": "World"}


#Signup API
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
    'email': fields.String,
    'role': fields.String
}

class UserApi(Resource):
    @marshal_with(user_fields)
    def get(self,query):
        return fetch_all_user()

    @marshal_with(user_fields)
    def post(self):
        args=user_data.parse_args()
        email= args['email']
        if validateSignup(email):
            user=signup(fname=args['fname'], lname= args['lname'], mobile=args['mobile'], email=args['email'], password=args['password'])
            return user
        else:
            pass

#Login API

login_data= reqparse.RequestParser()

login_data.add_argument('email')
login_data.add_argument('password')

class Login(Resource):

    def post(self):
        args=login_data.parse_args()
        email=args["email"]
        password=args['password']
        if Adminsignin(email, password):
            return 'Admin Logged in'
        elif Usersignin(email, password):
            return 'User Logged in'
        elif Managersignin(email, password):
            return 'Manager Logged in'
        else:
            return "Error"

#Admin Functionalities

cat=reqparse.RequestParser()
cat.add_argument('cat_name')

update_cat= reqparse.RequestParser()
update_cat.add_argument('edit_cat')

cat_fields={
    'name': fields.String,
    'id': fields.Integer
}

prod= reqparse.RequestParser()
prod.add_argument('prod_name')
prod.add_argument('mdate')
prod.add_argument('edate')
prod.add_argument('rate')
prod.add_argument('quantity')
# prod.add_argument('edit_prod')

prod_fields={
    'prod_name': fields.String,
    'manufacture_date': fields.String,
    'expiry_date': fields.String,
    'rate_per_unit': fields.Integer,
    'quantity': fields.Integer,
    'category_id': fields.Integer
}
class Category(Resource):
    @marshal_with(cat_fields)
    def get(self): #fetch all cat
        result=fetch_category()
        print(result)
        return result

    @marshal_with(cat_fields)
    def post(self):
        args=cat.parse_args()
        cat_name=args['cat_name']
        if validateCategory_name(cat_name):
            AddCategory(cat_name)
            return AddCategory(cat_name)
        else:
            return "Error"

class CategoryCRUD(Resource):
    @marshal_with(cat_fields)
    def get(self, id):
        return fetch_product_cat(id)

    @marshal_with(cat_fields)
    def put(self, id):
        args=update_cat.parse_args()
        new_name=args['name']
        if validateCategory_id(id):
            return EditCategory(new_name, id)
        else:
            return "Error"

    def delete(self, id):
        if validateCategory_id(id):
            return DeleteCategory(id)
        else:
            return "Error"

class Product(Resource):
    @marshal_with(prod_fields)
    def get(self,cat_id):
        return prodCat(cat_id)

    @marshal_with(prod_fields)
    def post(self, cat_id):
        args=prod.parse_args()
        prod_name=args['prod_name']
        mdate=args['mdate']
        edate= args['edate']
        rate= args['rate']
        quantity= args['quantity']
        if validateCategory_name(prod_name):
            AddProduct(prod_name, mdate, edate, rate, cat_id, quantity)
            print("Test")
            return 'Product created'
        else:
            return "Error"

class ProductCRUD(Resource):
    def get(self, prod_id):
        return prodCat(prod_id)

    def put(self, prod_id):
        args=prod.parse_args()
        prod_name = args['prod_name']
        mdate = args['mdate']
        edate = args['edate']
        rate = args['rate']
        quantity = args['quantity']
        if validateProduct(prod_id):
            return ProductUpdate(prod_id, prod_name, mdate, edate, rate, quantity)
        else:
            return "Error"

    def delete(self, prod_id):
        if validateProduct(prod_id):
            return DeleteProduct(prod_id)
        else:
            return "Error"

cart_data=reqparse.RequestParser()
cart_data.add_argument('product_id')
cart_data.add_argument('quantity')

cart_fields={
    "user_id": fields.Integer,
    "product_id": fields.Integer,
    "quantity": fields.Integer
}
class Cart(Resource):
    @marshal_with(cart_fields)
    def get(self, user_id):
        return cartProducts(user_id)

    @marshal_with(cart_fields)
    def post(self, user_id):
        args=cart_data.parse_args()
        product_id= args['product_id']

        return addcart(user_id, product_id)

class CartCRUD(Resource):
    def get(self,id, userid ):
        return None
    def put(self, id, userid):
        args= cart.parse_args()
        quantity= args['quantity']
        updateQuantity(userid, id, quantity)
        return "Quantity Updated"

    def delete(self, id, userid):

        deleteProductCart(userid, id)
        return "Deleted successfully"

product_name_field = fields.String(attribute=lambda x: x.name)
export_details={
    "product_name": product_name_field,
    "user_id":fields.Integer,
    "product_id":fields.Integer,
    "quantity":fields.Integer,
    "date_purchased": fields.String
}

export_data= reqparse.RequestParser()
# export_data.add_argument()
class exports(Resource):
    @marshal_with(export_details)
    def get(self):
        result= exportdetails()
        marshalled_result = [marshal(row, export_details) for row in result]

        return marshalled_result

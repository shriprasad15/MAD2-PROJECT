
from flask_restful import Resource, Api, marshal, reqparse, fields, marshal_with


from database import AddProduct, DeleteCategory, DeleteProduct, EditCategory, ProductUpdate, addcart, cartProducts, deleteProductCart, fetch_category, fetch_product_cat, prodCat, signup, updateQuantity, validateCategory_id, validateCategory_name, validateProduct, validateSignup, Adminsignin, Usersignin, Managersignin, fetch_all_user, AddCategory
from flask import abort, jsonify, request


from werkzeug.security import check_password_hash, generate_password_hash
from database import db
from task import send_welcome_msg, generate_csv

from flask_security import SQLAlchemySessionUserDatastore, Security, login_user, logout_user
from flask_security import current_user, auth_required, login_required, roles_required, roles_accepted,login_user, logout_user,auth_token_required

api = Api(prefix='/api')





class Homepage(Resource):
    def get(self):
        return {"hello": "World"}

user_data= reqparse.RequestParser()

user_data.add_argument('fname')
user_data.add_argument('lname')
user_data.add_argument('mobile')
user_data.add_argument('email')
user_data.add_argument('password')
user_data.add_argument('roles')
user_data.add_argument('username')

user_fields= {
    'fname': fields.String,
    'lname': fields.String,
    'mobile': fields.Integer,
    'email': fields.String,
    'get_roles': fields.List(fields.String),
}

class UserApi(Resource):
    @auth_required('token')
    @roles_required('admin')
    def get(self):
        print(request.headers)
        print(current_user)
        return marshal(fetch_all_user(), user_fields)



login_data= reqparse.RequestParser()

login_data.add_argument('email')
login_data.add_argument('password')

def get_user_roles(roles):
    return [role.name for role in roles]


class Login(Resource):

    def post(self):
        from models import User
        from app import find_user
        args=login_data.parse_args()
        email=args["email"]
        password=args['password']
        print(email, password)
        if Adminsignin(email, password):
            print("Admin logged in ")
            
            u1 = db.session.query(User).filter(User.email == email).first()
            # login_user(u1)
            token = generate_auth_token(u1,"admin", expires_in = 600)
            g.user = u1
            return token
        
        elif Usersign   in(email, password):
            print("aaaaagokul",current_user.is_authenticated)
            if current_user.is_authenticated:
                return "Log out first to login again"
            u1 = db.session.query(User).filter(User.email == email).first()
            login_user(u1)
            token = generate_auth_token(u1,"user", expires_in = 600)
            return token
        
        elif Managersignin(email, password):
            u1 = db.session.query(User).filter(User.email == email, User.password == password).first()
            token = jwt.encode({'user': u1.id, 'role': 'manager'}, "HashSecret", algorithm="HS256")
            return token
        else:
            return "Error"

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
        
#Admin Functionalities

cat=reqparse.RequestParser()
cat.add_argument('cat_name')

update_cat= reqparse.RequestParser()
update_cat.add_argument('edit_cat')

cat_fields={
    'name': fields.String,
    'id': fields.Integer,
    'message': fields.String
}

prod= reqparse.RequestParser()
prod.add_argument('prod_name')
prod.add_argument('mdate')
prod.add_argument('edate')
prod.add_argument('rate')
prod.add_argument('quantity')
# prod.add_argument('edit_prod')

prod_fields={
    'name': fields.String,
    'manufacture_date': fields.String,
    'expiry_date': fields.String,
    'rate_per_unit': fields.Integer,
    'quantity': fields.Integer,
    'category_id': fields.Integer
}
class Category_resource(Resource):
    # @marshal_with(cat_fields)
    @auth_required()
    # @login_required
    # @auth_token_required()
    @roles_required('user')
    def get(self): #fetch all cat
        # print(current_user)
        result=fetch_category()
        # print(result)
        return marshal(result, cat_fields)

    @marshal_with(cat_fields)
    def post(self):
        args=cat.parse_args()
        cat_name=args['cat_name']
        if validateCategory_name(cat_name):
            
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
        new_name=args['edit_cat']
        if validateCategory_id(id):
            return EditCategory(new_name, id)
        else:
            return "Error"

    def delete(self, id):
        if validateCategory_id(id):
            return DeleteCategory(id)
        else:
            return "Error"

class Product_API(Resource):
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
    @marshal_with(prod_fields)
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
        args= cart_fields.parse_args()
        quantity= args['quantity']
        updateQuantity(userid, id, quantity)
        return "Quantity Updated"

    def delete(self, id, userid):

        deleteProductCart(userid, id)
        return "Deleted successfully"

# product_name_field = fields.String(attribute=lambda x: x.name)
# export_details={
#     "product_name": product_name_field,
#     "user_id":fields.Integer,
#     "product_id":fields.Integer,
#     "quantity":fields.Integer,
#     "date_purchased": fields.String
# }
export_details = {
    "product_name": fields.String,
    "user_id": fields.Integer,
    "product_id": fields.Integer,
    "quantity": fields.Integer,
    "date_purchased": fields.String
}
export_data= reqparse.RequestParser()
# export_data.add_argument()
class exports(Resource):
    def get(self):
        data = generate_csv.delay()
        return "CSV file is being generated, you will receive a mail once done."

class Celery_API(Resource):
    def get(self):
        data = send_welcome_msg.delay("Hello Celery")
        return "Task completed"


api.add_resource(Homepage,'/')
api.add_resource(UserApi, '/user')

api.add_resource(Login, '/login_user')

api.add_resource(Category_resource, '/category') # get and post
api.add_resource(CategoryCRUD, "/category/<id>")

api.add_resource(Product_API, '/product/cat/<int:cat_id>')
api.add_resource(ProductCRUD,'/product/<prod_id>')

api.add_resource(Cart, '/cart/<user_id>')
api.add_resource(CartCRUD, '/cart/<id>/<userid>')

api.add_resource(exports, "/export")
api.add_resource(Celery_API, "/celery")


from flask import Flask,render_template,request,redirect,url_for,session
from flask_restful import Resource, Api
from config import Config
from workers import *

app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)
from models import *
from apis import *

api = Api(app)
api.add_resource(Homepage,'/')
api.add_resource(UserApi, '/user_signup')

api.add_resource(Category, '/category') # get and post
api.add_resource(CategoryCRUD, "/category/<id>")

api.add_resource(Product_API, '/product/cat/<int:cat_id>')
api.add_resource(ProductCRUD,'/product/<prod_id>')

api.add_resource(Cart, '/cart/<user_id>')
api.add_resource(CartCRUD, '/cart/<id>/<userid>')

api.add_resource(exports, "/export")

api.add_resource(Celery_API, "/celery")
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
print(celery)
@app.route("/add_data")
def add_data():
    p1=Profile(user_id=1,product_id=2,quantity=3)
    p2=Profile(user_id=1,product_id=2,quantity=3)
    p3=Profile(user_id=1,product_id=2,quantity=3)

    session.add(p1)
    session.add(p2)
    session.add(p3)
    session.commit()
    return "adsdas"


from sqlalchemy import func
@app.route("/get_accumulation_of_product")
def get_accumulation_of_product():
    p1=Profile(user_id=1,product_id=2,quantity=3)
    p2=Profile(user_id=1,product_id=2,quantity=3)
    p3=Profile(user_id=1,product_id=2,quantity=3)
    p4=Profile(user_id=1,product_id=3,quantity=3)

    session.add(p1)
    session.add(p2)
    session.add(p3)
    session.add(p4)
    session.commit()
    result = session.query(
        Product.name,
        Product.manufacture_date,
        Product.expiry_date,
        Product.rate_per_unit,
        Product.quantity,
        func.sum(Profile.quantity).label('total_quantity')
    ).join(Profile, Product.id == Profile.product_id).group_by(Product.id).all()
    print(result)
    for row in result:
        name, manufacture_date, expiry_date, rate_per_unit,qty_left, total_quantity = row
        print(f"Product Name: {name}, Manufacture Date: {manufacture_date}, Expiry Date: {expiry_date}, Rate per Unit: {rate_per_unit},qtyleft {qty_left}, Total Quantity: {total_quantity}")

    return "asdasd"
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
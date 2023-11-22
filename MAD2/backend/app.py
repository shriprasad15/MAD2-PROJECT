from flask import Flask,render_template,request,redirect,url_for,session
from flask_restful import Resource, Api
from config import Config
from workers import *
from flask_cors import CORS

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

from flask import send_file
@app.route('/download_csv')
def download_csv():
    return send_file(f'./instance/name.csv', as_attachment=True)

CORS(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
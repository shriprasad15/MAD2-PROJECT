from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, text
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

from flask import current_app as app
# from models import User, Category, Product, Cart, Profile


from datetime import datetime
def signup(fname, lname,mobile, email, password,role,is_active,is_approved):
    from models import User
    user=app.security.datastore.create_user( fname=fname, lname=lname,mobile=mobile, email=email, password=generate_password_hash(password), roles=[role])
    user.active=True
    # to return the user object, we need to commit the session

    db.session.commit()
    user1=db.session.query(User).filter(User.email==email).first()
    return user1

def validateSignup(email):
    from models import User
    u1 = db.session.query(User).filter(User.email == email).first()
    if u1:
        return False
    return True
def Usersignin(email, password):
    from models import User
    u1=db.session.query(User).filter(User.email==email).first()
    if u1 and check_password_hash(u1.password,password):
        if u1 and 'user' in u1.get_roles:
            print("user found")
            return u1
        else:
            print("user not found")
            return None
    else:
        print("user not found")
        return None
def fetch_user(userid):
    from models import User
    u1 = db.session.query(User).filter(User.id == userid).first()
    return u1
def fetch_all_user(filters=None):
    from models import User
    if not filters:
        u1= db.session.query(User).all()
    else:
        u1= db.session.query(User).filter_by(**filters).all()
    return u1

def addcart(userid, product_id):
    from models import Cart
    product_exist=db.session.query(Cart).filter(Cart.user_id == userid,Cart.product_id==product_id ).first()
    if product_exist is None:
        cart=Cart(user_id=userid, product_id=product_id, quantity=1)
        db.session.add(cart)
        db.session.commit()
        return cart
    else:
        product_exist.quantity += 1
        cart = product_exist
        db.session.commit()
        return cart


def cartProducts(userid):
    from models import User, Cart, Product
    cart=db.session.query(Cart).filter(Cart.user_id==userid ).all()
    return cart
def cartItems(userid, productid):
    from models import Cart
    items=db.session.query(Cart).filter(Cart.user_id==userid, Cart.product_id == productid).first()
    return items

def Adminsignin(email, password):
    from models import User
    # print(User.query.filter(User.email == email).first().password)
    # we need to check hashed password
    
    u1=db.session.query(User).filter(User.email==email).first()
    # print(check_password_hash(u1.password,password))
    print("Admin")
    print(u1)
    if u1 and 'admin' in u1.get_roles:
        return True
    else:
        False

def validateCategory_name(name):
    from models import Category
    u1 = db.session.query(Category).filter(Category.name == name).first()
    if u1:
        return False
    return True

def validateCategory_id(id):
    from models import Category
    u1 = db.session.query(Category).filter(Category.id == id).first()
    if u1:
        return True
    return False
def AddCategory(name):
    from models import Category
    category=Category(name=name)
    db.session.add(category)
    db.session.commit()
    return category

def DeleteCategory(id):
    from models import Category, Product
    category = db.session.query(Category).filter(Category.id == id).first()
    product= db.session.query(Product).filter(Product.category_id == category.id).all()
    if category:
        name=category.name
        db.session.delete(category)
        for item in product:
            db.session.delete(item)
        db.session.commit()
        return f"Category '{name}' has been deleted successfully."
    else:
        name = category.name
        return f"Category '{name}' not found."


def searchProduct(query):
    from models import Product, Category
    product = db.session.query(Product).filter(Product.name.ilike(f'%{query}%')).first()
    result=None
    if product:
        result = db.session.query(Product).filter(Product.name.ilike(f'%{query}%')).all()
        # return result

    else:
        category = db.session.query(Category).filter(Category.name.ilike(f'%{query}%')).first()
        # print(category)
        if category:
            category_id = category.id
            result = db.session.query(Product).filter(Product.category_id == category_id).all()
            # return result
    if not result:
        return None
    return result

    # return None

def EditCategory(newName, id):
    from models import Category
    category = db.session.query(Category).filter(Category.id == id).first()
    if category:
        oldName=category.name
        category.name=newName
        db.session.commit()
        response= category
        response.message =f"Category {oldName} has been changed to {newName}"
        return response
    
def fetch_category():
    from models import Category
    u1= db.session.query(Category).all()
    return u1
# AddProduct('Mango', datetime(2023,12,29), datetime(2024,1,10),'Rs/Kg',2, 150)
def fetch_product_cat(cat_id):
    from models import Category
    u1= db.session.query(Category).filter(Category.id== cat_id).first()
    return u1
def prodCat(catId):
    from models import Product
    u1=db.session.query(Product).filter(Product.category_id==catId).all()
    return u1
def fetch_all_products():
    from models import Product
    u1 = db.session.query(Product).all()
    return u1

def cart_prod(item):
    from models import Product

    return db.session.query(Product).get(item.product_id)
def search_user(name):
    from models import User

    u1=db.session.query(User).filter(User.fname== name).first()
    return u1

def cartPrice(prod):
    from models import Product, Cart
    for i in prod:
        p=db.session.query(Product).filter(Product.id==i.id).all()
        c=db.session.query(Cart).all()
        total_price=0
        for price in prod:
            for cart_quantity in c:
                if price.id==cart_quantity.product_id:
                    total_price+= int(price.rate_per_unit) * int(cart_quantity.quantity)
        return total_price

def updateQuantity(userid, product_id, quantity):
    from models import Cart
    item=db.session.query(Cart).filter(Cart.user_id==userid,Cart.product_id==product_id).first()
    item.quantity=quantity
    db.session.commit()
def deleteProductCart(userid, product_id):
    from models import Cart
    item = db.session.query(Cart).filter(Cart.user_id == userid, Cart.product_id == product_id).first()
    db.session.delete(item)
    db.session.commit()

def buyAll(userid):
    cart_items=db.session.query(Cart).filter(Cart.user_id==userid).all()
    for cart in cart_items:
        prod=db.session.query(Product).filter(Product.id==cart.product_id).first()
        if prod.quantity >= cart.quantity:
            prod.quantity-= cart.quantity
            now=datetime.now()
            date1=str(now.strftime("%d/%m/%Y %H:%M:%S"))
            profile_item = Profile(user_id=userid, product_id=cart.product_id, quantity=cart.quantity, date_purchased=date1)
            db.session.add(profile_item)
            db.session.delete(cart)
        else:
            return False
    db.session.commit()
    return True


def validateProduct(prod_id):
    u1 = db.session.query(Product).filter(Product.id == prod_id).first()
    if u1:
        return False
    return True
#To change Schema of addProduct
def AddProduct(name, manufacture_date, expiry_date, rate_per_unit, category_id, quantity):
    product=Product(name=name,  manufacture_date=manufacture_date, expiry_date=expiry_date, rate_per_unit=rate_per_unit, category_id=category_id, quantity=quantity)
    db.session.add(product)
    db.session.commit()

def DeleteProduct(id):

    product = db.session.query(Product).filter(Product.id == id).first()

    if product:
        name=product.name
        db.session.delete(product)
        db.session.commit()
        return f"Product '{name}' has been deleted successfully."
    else:
        name=product.name
        return f"Product '{name}' not found."
def ProductUpdate(prod_id, new_product_name, manufacture_date, expiry_date, rate_per_unit, quantity):
    existing_product = db.session.query(Product).filter_by(id=prod_id).first()

    if existing_product:
        if new_product_name:
            existing_product.name=new_product_name
        if manufacture_date:
            existing_product.manufacture_date = manufacture_date
        if expiry_date:
            existing_product.expiry_date = expiry_date
        if rate_per_unit:
            existing_product.rate_per_unit = rate_per_unit
        if quantity:
            existing_product.quantity = quantity


        db.session.commit()
        return f"Product has been deleted successfully."
    else:
        return f"Product Not found."
def profileItems(userid):
    profile_items = db.session.query(Product, Profile).join(Profile).filter(Product.id == Profile.product_id,Profile.user_id == userid).all()

    return profile_items

def purchase_items():
    result=db.session.query(Product, Profile).join(Profile).filter(Product.id == Profile.product_id, User.id==Profile.user_id).all()

    return result
def user_items():
    result=db.session.query(User).filter(User.id==Profile.user_id, User.role=='user').all()
    return result

def Managersignin(email, password):
    from models import User
    u1 = db.session.query(User).filter(User.email == email, User.password == password).first()
    if u1 and u1.role == 'manager':
        return u1
    else:
        return None

def exportdetails():
    from models import Profile, Product
    result = db.session.query(
        Product.name,
        Product.quantity,
        Product.rate_per_unit,
        func.sum(Profile.quantity).label('total_quantity')
    ).join(Profile, Product.id == Profile.product_id) \
        .group_by(Product.id).all()
    return result

def unit_sold(product_id):
    from models import Profile
    result= db.session.query(Profile).filter(Profile.product_id==product_id).all()
    s=0
    print("gokul")
    print(result)
    for r in result:
        s+=r.quantity
    print(s)
    return s



def fun():
  from models import User, Category, Product, Cart, Profile
  user1 = User(fname='Teddy',lname='Bear', email='teddy@mrbean.com', password='ted', role='admin', is_approved=True)
  user2 = User(fname='Ken',lname='Adams', email='ken@adams.com', mobile=1234,password='1234', role='user',is_approved=True)
  user3= User(fname='Shri',lname='Prasad', email='shri@prasad.com', mobile=5678,password='1111', role='manager',is_approved=False)
  category1 = Category(name='Fruits')
  category2 = Category(name='Snacks')

  product1 = Product(name='Apple', manufacture_date='2023-08-15', expiry_date='2023-08-19', rate_per_unit=90, category_id=1, quantity=20)
  product2 = Product(name='Watermelon', manufacture_date='2023-08-10', expiry_date='2023-08-15', rate_per_unit=40, category_id=1, quantity=15)
  product3 = Product(name='Potato Chips', manufacture_date='2023-07-30', expiry_date='2023-08-11', rate_per_unit=35, category_id=2, quantity=5)
  product4 = Product(name='Nachos', manufacture_date='2023-07-25', expiry_date='2023-07-30', rate_per_unit=50, category_id=2, quantity=3)

# Usage:


# engine = create_engine('sqlite:///grocery.db')
# db.Model.metadata.create_all(engine)

# Session2 = sessionmaker(bind=engine)



  with current_app.app_context():
      db.session.execute(text("DELETE FROM carts"))
      db.session.execute(text("DELETE FROM products"))
      db.session.execute(text("DELETE FROM categories"))
      db.session.execute(text("DELETE FROM users"))
      # db.session.execute(text("DELETE FROM profile"))
      db.session.commit()

      db.session.add_all([ user2,user1, user3,category1, category2, product1, product2, product3, product4])
      db.session.commit()


# app.app_context().push()

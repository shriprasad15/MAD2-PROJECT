from sqlalchemy import Column, Integer, String,Boolean, Date, ForeignKey,or_
from sqlalchemy.orm import relationship,declarative_base, joinedload
from datetime import datetime
from datetime import date
Base = declarative_base()

from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    fname = Column(String)
    lname = Column(String)
    mobile = Column(Integer)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
    is_approved = Column(Boolean)
    carts = relationship("Cart")
    def __repr__(self):
        return '<User %r>' % self.fname

class Profile(Base):
    __tablename__ = 'profile'

    id=Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    date_purchased=Column(String)
    def __repr__(self):
        return  str(self.product_id)+" "+str(self.quantity)

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    products = relationship("Product")
    is_approved= Column(Boolean)
    def __repr__(self):
        return '<Category %r>' % self.name

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String)
    manufacture_date = Column(String)
    expiry_date = Column(String)
    rate_per_unit = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    quantity= Column(Integer)
    profile = relationship("Profile")
    def __repr__(self):
        return '<Product %r>' % self.name

class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    def __repr__(self):
        # to return product name and quantity
        return  str(self.product_id)+" "+str(self.quantity)
        # return str(self.id) +" "+ str(self.user_id) +" "+ str(self.product_id)+" "+ str(self.quantity)

# Sample Data
# user1 = User(name='John Doe', email='john@example.com', password='password', role='admin')
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

engine = create_engine('sqlite:///grocery.db')
Base.metadata.create_all(engine)

Session2 = sessionmaker(bind=engine)
session = Session2()

session.execute(text("DELETE FROM carts"))
session.execute(text("DELETE FROM products"))
session.execute(text("DELETE FROM categories"))
session.execute(text("DELETE FROM users"))
# session.execute(text("DELETE FROM profile"))
session.commit()

session.add_all([ user2,user1, user3,category1, category2, product1, product2, product3, product4])
session.commit()




def signup(fname, lname,mobile, email, password):
    user1 = User(fname=fname, lname=lname,mobile=mobile, email=email, password=password, role='user')
    session.add(user1)
    session.commit()
    return user1
def validateSignup(email):
    u1 = session.query(User).filter(User.email == email).first()
    if u1:
        return False
    return True
def Usersignin(email, password):
    u1=session.query(User).filter(User.email==email, User.password==password).first()
    if u1 and u1.role=='user':
        return u1
    else:
        return None
def fetch_user(userid):
    u1 = session.query(User).filter(User.id == userid).first()
    return u1
def fetch_all_user(filters=None):
    if not filters:
        u1= session.query(User).all()
    else:
        u1= session.query(User).filter_by(**filters).all()
    return u1

def addcart(userid, product_id):
    product_exist=session.query(Cart).filter(Cart.user_id == userid,Cart.product_id==product_id ).first()
    if product_exist is None:
        cart=Cart(user_id=userid, product_id=product_id, quantity=1)
        session.add(cart)
        session.commit()
        return cart
    else:
        product_exist.quantity += 1
        cart = product_exist
        session.commit()
        return cart


def cartProducts(userid):
    cart=session.query(Cart).filter(Cart.user_id==userid ).all()
    return cart
def cartItems(userid, productid):
    items=session.query(Cart).filter(Cart.user_id==userid, Cart.product_id == productid).first()
    return items

def Adminsignin(email, password):
    u1=session.query(User).filter(User.email==email, User.password==password).first()
    if u1 and u1.role=='admin':
        return True
    else:
        False

def validateCategory_name(name):
    u1 = session.query(Category).filter(Category.name == name).first()
    if u1:
        return False
    return True

def validateCategory_id(id):
    u1 = session.query(Category).filter(Category.id == id).first()
    if u1:
        return True
    return False
def AddCategory(name):
    category=Category(name=name)
    session.add(category)
    session.commit()
    return category

def DeleteCategory(id):

    category = session.query(Category).filter(Category.id == id).first()
    product= session.query(Product).filter(Product.category_id == category.id).all()
    if category:
        name=category.name
        session.delete(category)
        for item in product:
            session.delete(item)
        session.commit()
        return f"Category '{name}' has been deleted successfully."
    else:
        name = category.name
        return f"Category '{name}' not found."


def searchProduct(query):
    product = session.query(Product).filter(Product.name.ilike(f'%{query}%')).first()
    result=None
    if product:
        result = session.query(Product).filter(Product.name.ilike(f'%{query}%')).all()
        # return result

    else:
        category = session.query(Category).filter(Category.name.ilike(f'%{query}%')).first()
        # print(category)
        if category:
            category_id = category.id
            result = session.query(Product).filter(Product.category_id == category_id).all()
            # return result
    if not result:
        return None
    return result

    # return None

def EditCategory(newName, id):
    category = session.query(Category).filter(Category.id == id).first()
    if category:
        oldName=category.name
        category.name=newName
        session.commit()
        return f"Category {oldName} has been changed to {newName}"
def fetch_category():
    u1= session.query(Category).all()
    return u1
# AddProduct('Mango', datetime(2023,12,29), datetime(2024,1,10),'Rs/Kg',2, 150)
def fetch_product_cat(cat_id):
    u1= session.query(Category).filter(Category.id== cat_id).first()
    return u1
def prodCat(catId):
    u1=session.query(Product).filter(Product.category_id==catId).all()
    return u1
def fetch_all_products():
    u1 = session.query(Product).all()
    return u1

def cart_prod(item):
    return session.query(Product).get(item.product_id)
def search_user(name):
    u1=session.query(User).filter(User.fname== name).first()
    return u1

def cartPrice(prod):
    for i in prod:
        p=session.query(Product).filter(Product.id==i.id).all()
        c=session.query(Cart).all()
        total_price=0
        for price in prod:
            for cart_quantity in c:
                if price.id==cart_quantity.product_id:
                    total_price+= int(price.rate_per_unit) * int(cart_quantity.quantity)
        return total_price

def updateQuantity(userid, product_id, quantity):
    item=session.query(Cart).filter(Cart.user_id==userid,Cart.product_id==product_id).first()
    item.quantity=quantity
    session.commit()
def deleteProductCart(userid, product_id):
    item = session.query(Cart).filter(Cart.user_id == userid, Cart.product_id == product_id).first()
    session.delete(item)
    session.commit()

def buyAll(userid):
    cart_items=session.query(Cart).filter(Cart.user_id==userid).all()
    for cart in cart_items:
        prod=session.query(Product).filter(Product.id==cart.product_id).first()
        if prod.quantity >= cart.quantity:
            prod.quantity-= cart.quantity
            now=datetime.now()
            date1=str(now.strftime("%d/%m/%Y %H:%M:%S"))
            profile_item = Profile(user_id=userid, product_id=cart.product_id, quantity=cart.quantity, date_purchased=date1)
            session.add(profile_item)
            session.delete(cart)
        else:
            return False
    session.commit()
    return True


def validateProduct(prod_id):
    u1 = session.query(Product).filter(Product.id == prod_id).first()
    if u1:
        return False
    return True
#To change Schema of addProduct
def AddProduct(name, manufacture_date, expiry_date, rate_per_unit, category_id, quantity):
    product=Product(name=name,  manufacture_date=manufacture_date, expiry_date=expiry_date, rate_per_unit=rate_per_unit, category_id=category_id, quantity=quantity)
    session.add(product)
    session.commit()

def DeleteProduct(id):

    product = session.query(Product).filter(Product.id == id).first()

    if product:
        name=product.name
        session.delete(product)
        session.commit()
        return f"Product '{name}' has been deleted successfully."
    else:
        name=product.name
        return f"Product '{name}' not found."
def ProductUpdate(prod_id, new_product_name, manufacture_date, expiry_date, rate_per_unit, quantity):
    existing_product = session.query(Product).filter_by(id=prod_id).first()

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


        session.commit()
        return f"Product has been deleted successfully."
    else:
        return f"Product Not found."
def profileItems(userid):
    profile_items = session.query(Product, Profile).join(Profile).filter(Product.id == Profile.product_id,Profile.user_id == userid).all()

    return profile_items

def purchase_items():
    result=session.query(Product, Profile).join(Profile).filter(Product.id == Profile.product_id, User.id==Profile.user_id).all()

    return result
def user_items():
    result=session.query(User).filter(User.id==Profile.user_id, User.role=='user').all()
    return result

def Managersignin(email, password):
    u1 = session.query(User).filter(User.email == email, User.password == password).first()
    if u1 and u1.role == 'manager':
        return u1
    else:
        return None

def exportdetails():
    result = session.query(
        Product.name,
        Product.quantity,
        Product.rate_per_unit,
        func.sum(Profile.quantity).label('total_quantity')
    ).join(Profile, Product.id == Profile.product_id) \
        .group_by(Product.id).all()
    return result
def unit_sold(product_id):
    result= session.query(Profile).filter(Profile.product_id==product_id).all()
    s=0
    print("gokul")
    print(result)
    for r in result:
        s+=r.quantity
    print(s)
    return s

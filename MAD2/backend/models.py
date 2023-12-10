
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Column, Integer, String,Boolean, Date, ForeignKey,or_
from sqlalchemy.orm import relationship,declarative_base, joinedload
from datetime import datetime
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from database import db

from flask import current_app as app


from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    fname = Column(String)
    lname = Column(String)
    mobile = Column(Integer)
    email = Column(String, unique=True)
    password = Column(String)
    is_authenticated = db.Column(db.Boolean())
    active = Column(Boolean, default=True)
    is_anonymous = Column(Boolean, default=False)
    is_approved = Column(Boolean)
    fs_uniquifier=Column(String)
    carts = relationship("Cart")
    roles = db.relationship('Role', secondary='user_roles',
                         backref=db.backref('users', lazy='dynamic'))
    
    @property
    def is_authorised(self):
        return self.authenticated
    
    # to return a list of roles as list of strings
    @property
    def get_roles(self):
        return [role.name for role in self.roles]
    
    def __repr__(self):
        return '<User %r>' % self.fname

class Role(db.Model):
        __tablename__ = 'roles'
        id = Column(Integer(), primary_key=True)
        name = Column(String(50), unique=True)

class UserRoles(db.Model):
        __tablename__ = 'user_roles'
        id = Column(Integer(), primary_key=True)
        user_id = Column(Integer(), ForeignKey('users.id', ondelete='CASCADE'))
        role_id = Column(Integer(), ForeignKey('roles.id', ondelete='CASCADE'))

    # Setup Flask-User and specify the User data-model
    

class Profile(db.Model):
    __tablename__ = 'profile'

    id=Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    date_purchased=Column(String)
    def __repr__(self):
        return  str(self.product_id)+" "+str(self.quantity)

class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    products = relationship("Product")
    is_approved= Column(Boolean)
    def __repr__(self):
        return '<Category %r>' % self.name

class Product(db.Model):
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

class Cart(db.Model):
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

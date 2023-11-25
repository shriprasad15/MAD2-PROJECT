from sqlalchemy import Column, Integer, String,Boolean, Date, ForeignKey,or_
from sqlalchemy.orm import relationship,declarative_base, joinedload
from flask_security import UserMixin, RoleMixin
Base = declarative_base()
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    fname = Column(String)      
    lname = Column(String)
    mobile = Column(Integer)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
    authenticated= Column(Boolean)
    fs_uniquifier= Column(String, unique=True, nullable=False)

    is_approved = Column(Boolean)
    
    carts = relationship("Cart")
    roles= relationship("Role", secondary="role_users", backref="user", lazy='dynamic')

    @property
    def is_autherized(self):
        return self.is_authenticated
    

class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('users.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))
    
class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)

    @classmethod
    def query(cls):
        return session.query(cls)



engine = create_engine('sqlite:///grocery.db')
Base.metadata.create_all(engine)

Session2 = sessionmaker(bind=engine)
session = Session2()
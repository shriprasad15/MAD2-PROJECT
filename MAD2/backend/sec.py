from flask_security import SQLAlchemySessionUserDatastore
from models import db, User, Role
datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
from app import db
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    __tablename__= 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    date_created = Column(db.DateTime, index=True, default=datetime.utcnow)
    password_hash = Column(String(128))

    def __repr__(self):
        return '<User {}>'.format(self.name)   

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 


class Category(db.Model):
    __tablename__= 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    description = Column(String(256))
    date_created = Column(db.DateTime, index=True, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Category {}>'.format(self.name)



class Item(db.Model):
    __tablename__= 'item'
    id = Column(Integer, primary_key=True)
    title = Column(String(140), nullable=True)
    description = Column(String(256))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    def __repr__(self):
        return '<Item {}>'.format(self.title)




@login.user_loader
def load_user(id):
    return User.query.get(int(id))
from bcrypt import checkpw, gensalt, hashpw
# from connectors.db import Base
# from flask_login import UserMixin
# from sqlalchemy import Column, Enum, Integer, String, Text, DateTime, ForeignKey, func
# from sqlalchemy.orm import relationship 
# from flask_sqlalchemy import SQLAlchemy
from extensions import db

# db = SQLAlchemy() 

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Enum('admin', 'user'), nullable=False, default='user')


    
    
    def set_password(self, password):
        self.password = hashpw(password.encode('utf-8'),  gensalt()).decode('utf-8')

    def check_password(self, password):
        return checkpw(password.encode("utf-8")), self.password.encode("utf-8")
    
    # reviews = relationship("UserReviewModel", back_populates="user")
    def __repr__(self):
        return f'<UserModel(id={self.id}, username={self.username}, email={self.email})>'


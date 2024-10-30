from connectors.db import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
# from flask_sqlalchemy import SQLAlchemy
from extensions import db

# db = SQLAlchemy()
class UserReviewModel(db.Model):
    __tablename__ = 'user_reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    review = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # created_at = Column(DateTime(timezone=True), server_default=func.now())

    # user = relationship("UserModel", back_populates="reviews")
    user = relationship("UserModel", back_populates="user_reviews")

class UserModel(db.Model):
    __tablename__ = 'users'
    review = relationship("UserReviewModel", back_populates="users")

    def __repr__(self):
        return f'<UserReviewModel(user_review_id={self.user_review_id}, user_id={self.user_id}, rating={self.rating}), review={self.review})>'
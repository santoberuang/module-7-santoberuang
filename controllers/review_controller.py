from flask import Blueprint, redirect, request, url_for
from flask_login import current_user
from services.user_service import role_required
from models.user_review_model import UserReviewModel
from connectors.db import Session

reviewBp = Blueprint('review', __name__)

@reviewBp.route('/review', methods=['POST'])
@role_required('admin')
def add_review():
    description = request.form.get('review')
    rating = request.form.get('rating')
    # print(description, rating)

    if description is None or rating is None:
        return redirect(url_for('display.review', error='Please fill out the form completely!'))
    
    try:
        with Session() as session:
            user_review = UserReviewModel(description=description, rating=int(rating), user_id=current_user.user_id)
            session.add(user_review)
            session.commit()

            return redirect(url_for('display.review'))
        
    except Exception as e:
        print(e)
        session.rollback()
        return redirect(url_for('display.review'), 'Error adding review. Please Try Agin')

@reviewBp.route('/review/update', methods=['POST'])
@role_required('admin')
def update_review():
    user_review_id = request.form.get('id')
    description = request.form.get('review')
    rating = request.form.get('rating')
    print(description, rating)

    try:
        with Session() as session:
            user_review = session.query(UserReviewModel).get(user_review_id)
            user_review.review = description
            user_review.rating = rating
            session.commit()

            return redirect(url_for('display.review'))
        
    except Exception as e:
        print(e)
        session.rollback()
        return redirect(url_for('display.review'), 'Error updating review. Please Try Agin')

@reviewBp.route('/review/delete', methods=['POST'])
@role_required('admin')
def delete_review():
    user_review_id = request.form.get('id')
    print(user_review_id)

    try:
        with Session() as session:
            user_review = session.query(UserReviewModel).get(user_review_id)
            session.delete(user_review)
            session.commit()

            return redirect(url_for('display.review'))
        
    except Exception as e:
        print(e)
        session.rollback()
        return redirect(url_for('display.review'), 'Error deleting review. Please Try Agin')
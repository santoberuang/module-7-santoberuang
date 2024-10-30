from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from services.user_service import role_required
from connectors.db import Session
from models.user_review_model import UserReviewModel

displayBp = Blueprint('display', __name__)

@displayBp.route('/')
def index():
    return render_template('index.html', current_user=current_user)


@displayBp.route('/login', methods=['GET'])
def login():
    error = request.args.get('error')
    return render_template('login.html', current_user=current_user, error=error)


@displayBp.route('/register', methods=['POST'])
def register(): 
    error = request.args.get('error')
    return render_template('register.html', current_user=current_user, error=error)

@displayBp.route('/home')
@login_required
def home():
    return render_template('home.html')

@displayBp.route('/review')
@login_required
@role_required('admin')
def review():
    try:
        with Session() as session:
            user_reviews = session.query(UserReviewModel).all()
        return render_template('review.html', current_user=current_user, user_reviews=user_reviews)

    except Exception as e:
        print(e)
        return redirect(url_for('display.review'), 'Error getting reviews. Please Try Agin'), 500

@displayBp.route('/review/create', methods=['GET'])
@login_required
@role_required('admin')
def create_review():
    error = request.args.get('error')
    return render_template('create_review.html', current_user=current_user, error=error)

@displayBp.route("/review/update", methods=['GET'])
@login_required
@role_required('admin')
def update_review():
    error = request.args.get('error')
    user_review_id = request.args.get('user_review_id')

    try:
        with Session() as session:
            user_review = session.query(UserReviewModel).get(user_review_id)
            return render_template('update_review.html', current_user=current_user, error=error, user_review=user_review)

    except Exception as e:
        print(e)
        return render_template('update_review.html', user_review=[], current_user=current_user, error=error), 500


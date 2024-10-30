import datetime
from flask import Blueprint, jsonify, redirect, request, url_for
from flask_jwt_extended import create_access_token, unset_jwt_cookies
from flask_login import login_required, login_user, logout_user
from connectors.db import Session
from models.user_model import UserModel



userBp = Blueprint('user', __name__)


@userBp.route('/login', methods=['POST'])
def user_login():
    # data = request.json
    email = request.form.get('email')
    password = request.form.get('password')
    print( f'logging in user', email, password)

    if email is None or password is None:
        return redirect(url_for('display.login', error='Please fill out the form completely!'))
    
    try:
        with Session() as session:
            user = session.query(UserModel).filter(UserModel.email == email).first()
            isCorrectUser = user and user.check_password(password)
            
            if isCorrectUser:
                login_user(user)
                expires = datetime.timedelta(minutes=120)
                create_access_token(identity={
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                } , expires_delta=expires)
                return jsonify({'redirect': url_for('display.home')}), 200
            else:
                return redirect(url_for('display.login', error='Invalid email or passwordæ'))
    except Exception as e:
            print(e)
            session.rollback()
            return redirect(url_for('display.login', error='Error logging in user'))



@userBp.route('/register', methods=['POST'])
def user_register():
    # data = request.json
    username = request.form.get('username')
    email = request.form.get('email')
    role = request.form.get('role')
    password = request.form.get('password')
    # print( f'registering user', username, email, role, password)

    if username is None or email is None or role is None or password is None:
        return redirect(url_for('display.register', error='Please fill out the form completely!'))
    
    try:
        with Session() as session:
    
            user = UserModel(username=username, email=email, role=role)
            user.set_password(password)

            session.add(user)
            session.commit()

            login_user(user)
            expires = datetime.timedelta(minutes=120)
            create_access_token(identity={
                'user_id': user.id,
                'username': user.username,
                'role': user.role
            }, expires_delta=expires)

            return jsonify({'redirect': url_for('display.home')}), 200
        
    except Exception as e:
            print(e)
            session.rollback()
            return redirect(url_for('display.register', error='Error creating user. Please try again!'))
    
@userBp.route('/logout', methods=['POST'])
@login_required
def user_logout():
    try:
        response = jsonify({'message': 'Successfully logged out'})
        logout_user()
        unset_jwt_cookies(response)
        return jsonify({'redirect': url_for('display.login')}), 200
    
    except Exception as e:
        print(e)
    return jsonify({'error': 'You are not logged out'}), 500
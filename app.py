from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from connectors.db import connection, Base, Session
from models.user_model import UserModel
from controllers.user_controller_check import userBp
from controllers.display_controller import displayBp
from controllers.review_controller import reviewBp
import os
from flask_login import LoginManager, login_required
from flask_jwt_extended import JWTManager
from extensions import db
from models.user_review_model import UserReviewModel
from models.user_model import UserModel

# Base.metadata.create_all(connection)


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional

# db = SQLAlchemy(app) 
db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(userBp)
app.register_blueprint(displayBp)
app.register_blueprint(reviewBp)


@login_manager.user_loader
def load_user(user_id):
    try:
        with Session() as session:
            return session.query(UserModel).get(user_id)
    except Exception as e:
        print(e)
        return None
    


@login_manager.unauthorized_handler
def unauthorized_callback():
    return render_template('display.unauthorized')
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

bcrypt = Bcrypt()
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
mail = Mail()
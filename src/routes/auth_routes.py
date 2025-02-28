from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

from src.extensions.extensions import bcrypt, db
from src.messages.response_message import ResponseMessage
from src.model.user import User
from src.schemas.login_template import user_login_request_schema

users_blueprint = Blueprint("users_blueprint", __name__, url_prefix="/api/v1/users")

@users_blueprint.route("/login", methods=['POST'])
def authenticate_user():
    request_json = request.get_json()

    try:
        validate(instance=request_json, schema=user_login_request_schema)
    except ValidationError as exc:
        response_message = ResponseMessage(exc.message, 400)
        return response_message.create_response_message()

    fetched_user = User.query.filter_by(email_address=request.get_json()["username"]).first()
    if not fetched_user:
        response_message = ResponseMessage("User was not found", 404)
        return response_message.create_response_message()

    if not bcrypt.check_password_hash(fetched_user.password, request.get_json()["password"]):
        response_message = ResponseMessage("Invalid username/password", 400)
        return response_message.create_response_message()

    response_message = ResponseMessage(create_access_token(fetched_user.email_address), 200)
    return response_message.create_response_message()


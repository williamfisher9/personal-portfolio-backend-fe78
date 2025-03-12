from flask import Blueprint, request, send_from_directory
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from src.messages.response_message import ResponseMessage
from src.extensions.extensions import db
import os
import json
import logging

from src.model.portfolio import Portfolio
from src.model.stored_images import StoredImages

portfolio_blueprint = Blueprint("portfolio_blueprint", __name__, url_prefix="/api/v1/portfolio")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

logger = logging.getLogger(__name__)

def get_param_value_by_name(val):
    with open('src//extensions//configs.json', 'r') as props_file:
        return json.load(props_file)[val]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_profile_img_link(filename):
    if filename:
        return get_param_value_by_name("WEB_SERVER_NAME") + "/portfolio/api/v1/portfolio/images/" + filename
        #return url_for("blog_blueprint.get_img_url", _external=True, filename=filename)

@portfolio_blueprint.route('/images/<filename>', methods=['GET'])
def get_img_url(filename):
   return send_from_directory(get_param_value_by_name("UPLOAD_FOLDER"), filename, as_attachment=False)


@portfolio_blueprint.route("/items", methods=['GET'])
def get_all_portfolio_items():
    logger.info(request.remote_addr)
    portfolio_items = Portfolio.query.all()

    for item in portfolio_items:
        item.main_image_source = get_profile_img_link(item.main_image_source)

    response_message = ResponseMessage([item.to_dict() for item in portfolio_items], 200)
    return response_message.create_response_message()

@portfolio_blueprint.route("/items/new", methods=['POST'])
@jwt_required()
def create_portfolio_item():
    if 'file' not in request.files:
        response_message = ResponseMessage("File was not found in the request", 400)
        return response_message.create_response_message()

    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        response_message = ResponseMessage("Improper file name", 400)
        return response_message.create_response_message()

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(get_param_value_by_name("UPLOAD_FOLDER"), filename))

        portfolio_item = Portfolio(request.form['title'],
                    request.form['description'],
                    request.form['link'],
                    filename)
        db.session.add(portfolio_item)
        db.session.commit()

        response_message = ResponseMessage("portfolio item created successfully", 201)
        return response_message.create_response_message()


@portfolio_blueprint.route("/items/<id>", methods=['GET'])
def get_portfolio_item_by_id(id):
    portfolio_item = Portfolio.query.filter_by(id=id).first()
    if not portfolio_item:
        response_message = ResponseMessage("Portfolio item was not found", 404)
        return response_message.create_response_message()
    else:
        portfolio_item.main_image_source = get_profile_img_link(portfolio_item.main_image_source)
        response_message = ResponseMessage(portfolio_item.to_dict(), 200)
        return response_message.create_response_message()

@portfolio_blueprint.route("/items/<id>", methods=['DELETE'])
@jwt_required()
def delete_portfolio_item_by_id(id):
    portfolio_item = Portfolio.query.filter_by(id=id).first()
    if not portfolio_item:
        response_message = ResponseMessage("Portfolio item was not found", 404)
        return response_message.create_response_message()
    else:
        db.session.delete(portfolio_item)
        db.session.commit()

        response_message = ResponseMessage("Portfolio item deleted successfully", 200)
        return response_message.create_response_message()

@portfolio_blueprint.route("/items/update/<id>", methods=['PUT'])
@jwt_required()
def update_portfolio_item(id):
    fetched_portfolio_item = Portfolio.query.filter_by(id=id).first()

    if not fetched_portfolio_item:
        response_message = ResponseMessage("Portfolio item was not found", 404)
        return response_message.create_response_message()

    if 'file' not in request.files:
        fetched_portfolio_item.title = request.form['title']
        fetched_portfolio_item.description = request.form['description']
        fetched_portfolio_item.link = request.form['link']
        db.session.add(fetched_portfolio_item)
        db.session.commit()

        response_message = ResponseMessage("Portfolio item updated successfully", 201)
        return response_message.create_response_message()


    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        response_message = ResponseMessage("Improper file name", 400)
        return response_message.create_response_message()

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(get_param_value_by_name("UPLOAD_FOLDER"), filename))

        fetched_portfolio_item.title = request.form['title']
        fetched_portfolio_item.description = request.form['description']
        fetched_portfolio_item.link = request.form['link']
        fetched_portfolio_item.main_image_source = filename
        
        db.session.add(fetched_portfolio_item)
        db.session.commit()

        response_message = ResponseMessage("Portfolio item updated successfully", 201)
        return response_message.create_response_message()
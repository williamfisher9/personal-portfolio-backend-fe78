from flask import Blueprint, request
from flask_mail import Message

from src.extensions.extensions import mail
import os
import logging

mail_blueprint = Blueprint("mail_blueprint", __name__, url_prefix="/api/v1/mail")

logging.getLogger(__name__)

@mail_blueprint.route("/send", methods=['POST'])
def send_email():
    logging.info("received a request to send an email")
    logging.info(request.get_json()['name'])
    logging.info(request.get_json()['mail'])
    logging.info(request.get_json()['message'])
    msg = Message(request.get_json()['name'] , sender=request.get_json()['mail'], recipients=[os.environ.get('MAIL_USERNAME')])
    msg.body = request.get_json()['message']
    mail.send(msg)
    return "Sent", 200
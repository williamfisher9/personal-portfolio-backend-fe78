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
    logging.info(request.get_json())
    msg = Message(request.get_json()['name'] , sender=os.environ.get('MAIL_USERNAME'), recipients=[os.environ.get('MAIL_USERNAME')])
    msg.html = f"<div><h1>Sender: {request.get_json()['mail']}</h1><p>{request.get_json()['message']}</p></div>"
    mail.send(msg)
    return "Sent", 200
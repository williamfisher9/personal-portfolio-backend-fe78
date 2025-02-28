from flask import Blueprint, request
from flask_mail import Message

from src.extensions.extensions import mail
import os

mail_blueprint = Blueprint("mail_blueprint", __name__, url_prefix="/api/v1/mail")

@mail_blueprint.route("/send", methods=['POST'])
def send_email():
    msg = Message(request.get_json()['name'] , sender=os.environ.get('MAIL_USERNAME'), recipients=[os.environ.get('MAIL_USERNAME')])
    msg.body = request.get_json()['message']
    mail.send(msg)
    return "Sent", 200
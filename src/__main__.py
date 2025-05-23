from logging import Logger

from flask import Flask

from src.extensions.app_config import initialize_app
from src.extensions.extensions import bcrypt, db, jwt, cors, mail

import json
import os

from src.extensions.initialize_database import initialize_database
from src.routes.auth_routes import users_blueprint
from src.routes.blog_routes import blog_blueprint
from src.routes.mail_routes import mail_blueprint

import logging

from src.routes.portfolio_routes import portfolio_blueprint

if __name__ == '__main__':
    initialize_app()

    logger = logging.getLogger(__name__)
    logger.info("initializing app instance")

    app = Flask(__name__)
    app.config.from_file("extensions//configs.json", load=json.load)
    app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD')

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    mail.init_app(app)

    logging.info("registering blueprints")

    app.register_blueprint(users_blueprint)
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(mail_blueprint)
    app.register_blueprint(portfolio_blueprint)

    with app.app_context():
        logging.info("initializing database instance")
        initialize_database()

    logging.info("finished initializing app instance")
    logging.info("starting the app")
    app.run(debug=True, port=9999)

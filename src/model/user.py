from flask_login import UserMixin
from src.extensions.extensions import db

class User(db.Model, UserMixin):
    __tablename__ = "users"

    def __init__(self, first_name, last_name, email_address, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.password = password

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False, unique=False)
    last_name = db.Column(db.String(20), nullable=False, unique=False)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    roles = db.Relationship('Role', secondary = 'user_roles', back_populates = 'user')

    def __repr__(self):
        return f"<User {self.id} {self.email_address}>"

    def __str__(self):
        return f"User {self.id} {self.email_address} {self.first_name} {self.last_name}"


from src.extensions.extensions import db

class Role(db.Model):
    __tablename__ = "roles"

    def __init__(self, name):
        self.name = name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    user = db.Relationship('User', secondary = 'user_roles', back_populates = 'roles')

    user_roles = db.Table("user_roles",
        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
    )

    def __repr__(self):
        return f"<Role {self.name}>"

    def __str__(self):
        return f"Role {self.id} {self.name}"
from src.extensions.extensions import db

class StoredImages(db.Model):
    def __init__(self, name, source):
        self.name = name
        self.source = source

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    source = db.Column(db.Text(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "source": self.source
        }

    def __repr__(self):
        return f"<Image {self.name}>"

    def __str__(self):
        return f"Image {self.id} {self.name}"
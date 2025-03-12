import datetime

from src.extensions.extensions import db

class Portfolio(db.Model):
    def __init__(self, title, description, link, main_image_source):
        self.title = title
        self.description = description
        self.link = link
        self.main_image_source = main_image_source

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    main_image_source = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "link": self.link,
            "main_image_source": self.main_image_source
        }

    def __repr__(self):
        return f"<Portfolio {self.title}>"

    def __str__(self):
        return f"Portfolio {self.id} {self.title}"
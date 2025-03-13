import datetime
from email.policy import default

from src.extensions.extensions import db

class Blog(db.Model):
    def __init__(self, title, description, post_contents, main_image_source, project_id):
        self.title = title
        self.description = description
        self.post_contents = post_contents
        self.main_image_source = main_image_source
        self.project_id = project_id

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    post_contents = db.Column(db.Text(), nullable=False)
    main_image_source = db.Column(db.Text(), nullable=False)
    project_id = db.Column(db.Integer, nullable=True)
    blog_creation_date = db.Column(db.DateTime, default=datetime.datetime.now())
    blog_update_date = db.Column(db.DateTime, default=datetime.datetime.now())

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "post_contents": self.post_contents,
            "main_image_source": self.main_image_source,
            "project_id": self.project_id,
            "blog_creation_date": self.blog_creation_date,
            "blog_update_date": self.blog_update_date
        }

    def __repr__(self):
        return f"<Blog {self.title}>"

    def __str__(self):
        return f"Blog {self.id} {self.title}"
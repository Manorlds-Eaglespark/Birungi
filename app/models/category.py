import uuid
from datetime import datetime
from shared import db, ma

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    icon_image = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, category_object):
        """Initialize a category object"""
        now = datetime.now()
        self.name = category_object["name"]
        self.description = category_object["description"]
        self.icon_image = category_object["icon_image"]
        self.created_on = datetime.timestamp(now)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "icon_image", "created_on")

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
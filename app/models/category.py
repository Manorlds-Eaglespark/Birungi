import uuid
from datetime import datetime
from shared import db, ma
from app.models.users import User

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    icon_url = db.Column(db.String(255))
    icon_delete_hash = db.Column(db.String(255))
    created_by= db.Column(db.Integer, db.ForeignKey(User.id))
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', backref='category')

    def __init__(self, category_object):
        """Initialize a category object"""
        now = datetime.now()
        self.name = category_object["name"]
        self.description = category_object["description"]
        self.icon_url = category_object["icon_url"]
        self.icon_delete_hash = category_object["icon_delete_hash"]
        self.created_by = category_object["created_by"]
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def add_added(self, category_data):
        if category_data['name'] != '':
            self.name = category_data['name']
        if category_data['description'] != '':
            self.description = category_data['description']
        if category_data['icon_url'] != '':
            self.icon_url = category_data['icon_url']


class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "icon_url", "created_by", "created_on")

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
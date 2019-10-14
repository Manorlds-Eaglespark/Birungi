import uuid
from datetime import datetime
from shared import db, ma
from app.models.product import Product


class Photo(db.Model):
    
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id))
    url = db.Column(db.String(255))
    product = db.relationship('Product', backref='photo')

    def __init__(self, photo_data):
        """Initialize an photo object"""
        self.product_id = photo_data["product_id"]
        self.url = photo_data["url"]

class PhotoSchema(ma.Schema):
    class Meta:
        fields = ("id", "product_id", "url")

photo_schema = PhotoSchema()
photos_schema = PhotoSchema(many=True)

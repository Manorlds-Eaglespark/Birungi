import uuid
from datetime import datetime
from shared import db, ma
from app.models.product import Product


class Amenity(db.Model):
    
    __tablename__ = 'amenities'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id))
    description = db.Column(db.String(255))
    product = db.relationship('Product', backref='amenity')

    def __init__(self, product_id, description):
        """Initialize an amenity object"""
        self.product_id = product_id
        self.description = description

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class AmenitySchema(ma.Schema):
    class Meta:
        fields = ("id", "description")

amenity_schema = AmenitySchema()
amenities_schema = AmenitySchema(many=True)

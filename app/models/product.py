import uuid
from datetime import datetime
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType
from shared import db, ma
from app.models.category import Category


class Product(db.Model):
    
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))
    description = db.Column(db.String(255))
    dimensions = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    search_vector = db.Column(TSVectorType('name', 'brand', 'description'))
    category = db.relationship('Category', backref='product')

    def __init__(self, product_data):
        """Initialize an product object"""
        now = datetime.now()
        self.name = product_data["name"]
        self.price = product_data["price"]
        self.brand = product_data["brand"]
        self.category = product_data["category"]
        self.description = product_data["description"]
        self.dimensions = product_data["dimensions"]
        self.created_on = datetime.timestamp(now)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def add_added(self, product_data):
        if product_data["name"] != '':
            self.name = product_data["name"]
        if product_data["price"] != '':
            self.price = product_data["price"]
        if product_data["brand"] != '':
            self.brand = product_data["brand"]
        if product_data["category"] != '':
            self.category = product_data["category"]
        if product_data["description"] != '':
            self.description = product_data["description"]
        if product_data["dimensions"] != '':
            self.dimensions = product_data["dimensions"]


class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "price", "brand", "category", "description", "dimensions", "created_on")

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

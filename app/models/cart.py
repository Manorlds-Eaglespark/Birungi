import uuid
from datetime import datetime
from shared import db, ma
from app.models.users import User

class Cart(db.Model):
    __tablename__ = 'carts '
    id = db.Column(db.Integer, primary_key=True)
    item_list = db.Column(db.String(255))
    item_qty = db.Column(db.String(255))
    status = db.Column(db.String(15))
    created_by= db.Column(db.Integer, db.ForeignKey(User.id))
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', backref='cart')

    def __init__(self, cart_object):
        """Initialize a category object"""
        self.item_list = cart_object["item_list"]
        self.item_qty = cart_object["item_qty"]
        self.status = cart_object["status"]
        self.created_by = cart_object["created_by"]
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def add_added(self, cart_status):
        if cart_status != '':
            self.status = cart_status


class CartSchema(ma.Schema):
    class Meta:
        fields = ("id", "item_list", "item_qty", "status", "created_by", "created_on")

cart_schema = CartSchema()
carts_schema = CartSchema(many=True)

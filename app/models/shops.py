from shared import db, ma
from app.models.category import Category
from app.models.users import User



class Shop(db.Model):
    
    __tablename__ = 'shops'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    owner = db.Column(db.Integer, db.ForeignKey(User.id))
    address = db.Column(db.String(255))
    email = db.Column(db.String(50))
    telephone_1 = db.Column(db.String(255))
    telephone_2 = db.Column(db.String(255))
    short_brief = db.Column(db.String(255))
    description = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', backref='shop')
   

    def __init__(self, shop_data):
        """Initialize an shop object"""
        self.name = shop_data["name"]
        self.owner = shop_data["owner"]
        self.address = shop_data["address"]
        self.email = shop_data["email"]
        self.telephone_1 = shop_data["telephone_1"]
        self.telephone_2 = shop_data["telephone_2"]
        self.short_brief = shop_data["short_brief"]
        self.description = shop_data["description"]
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def add_added(self, shop_data):
        if shop_data["name"] != '':
            self.name = shop_data["name"]
        if shop_data["address"] != '':
            self.address = shop_data["address"]
        if shop_data["email"] != '':
            self.email = shop_data["email"]
        if shop_data["telephone_1"] != '':
            self.telephone_1 = shop_data["telephone_1"]
        if shop_data["telephone_2"] != '':
            self.telephone_2 = shop_data["telephone_2"]
        if shop_data["brief"] != '':
            self.short_brief = shop_data["brief"]
        if shop_data["description"] != '':
            self.description = shop_data["description"]

class ShopSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "owner", "address", "email", "telephone_1", "telephone_2", "short_brief", "description", "created_on")

shop_schema = ShopSchema()
shops_schema = ShopSchema(many=True)

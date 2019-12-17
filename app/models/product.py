from shared import db, ma
from app.models.category import Category
from app.models.users import User
from app.models.shops import Shop

class Product(db.Model):
    
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.String(9))
    brand = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))
    shop_id = db.Column(db.Integer, db.ForeignKey(Shop.id))
    measurements = db.Column(db.String(255))
    description = db.Column(db.String(255))
    image_1_url = db.Column(db.String(255))
    image_1_delete_hash = db.Column(db.String(255))
    image_2_url = db.Column(db.String(255))
    image_2_delete_hash = db.Column(db.String(255))
    image_3_url = db.Column(db.String(255))
    image_3_delete_hash = db.Column(db.String(255))
    image_4_url = db.Column(db.String(255))
    image_4_delete_hash = db.Column(db.String(255))
    detail_1 = db.Column(db.String(255))
    detail_2 = db.Column(db.String(255))
    detail_3 = db.Column(db.String(255))
    detail_4 = db.Column(db.String(255))
    detail_5 = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    category = db.relationship('Category', backref='product')
    user = db.relationship('User', backref='product')
    shop = db.relationship('Shop', backref='product')


    def __init__(self, product_data):
        """Initialize an product object"""
        self.name = product_data["name"]
        self.price = product_data["price"]
        self.brand = product_data["brand"]
        self.category_id = product_data["category_id"]
        self.shop_id = product_data["shop_id"]
        self.measurements = product_data["measurements"]
        self.description = product_data["description"]
        self.image_1_url = product_data["image_1_url"]
        self.image_1_delete_hash = product_data["image_1_delete_hash"]
        self.image_2_url = product_data["image_2_url"]
        self.image_2_delete_hash = product_data["image_2_delete_hash"]
        self.image_3_url = product_data["image_3_url"]
        self.image_3_delete_hash = product_data["image_3_delete_hash"]
        self.image_4_url = product_data["image_4_url"]
        self.image_4_delete_hash = product_data["image_4_delete_hash"]
        self.detail_1 = product_data["detail_1"]
        self.detail_2 = product_data["detail_2"]
        self.detail_3 = product_data["detail_3"]
        self.detail_4 = product_data["detail_4"]
        self.detail_5 = product_data["detail_5"]
        self.created_by = product_data["created_by"]
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __eq__(self, other):
        return self.name==other.name\
           and self.brand==other.brand

    def add_added_detail(self, product_data):
        if product_data['name'] != '':
            self.name = product_data['name']
        if product_data['price'] != '':
            self.price = product_data['price']
        if product_data['brand'] != '':
            self.brand = product_data['brand']
        if product_data['measurements'] != '':
            self.measurements = product_data['measurements']
        if product_data['description'] != '':
            self.description = product_data['description']
        if product_data['image_1_url'] != '':
            self.image_1_url = product_data['image_1_url']
        if product_data['image_1_delete_hash'] != '':
            self.image_1_delete_hash = product_data['image_1_delete_hash']
        if product_data['image_2_url'] != '':
            self.image_2_url = product_data['image_2_url']
        if product_data['image_2_delete_hash'] != '':
            self.image_2_delete_hash = product_data['image_2_delete_hash']
        if product_data['image_3_url'] != '':
            self.image_3_url = product_data['image_3_url']
        if product_data['image_3_delete_hash'] != '':
            self.image_3_delete_hash = product_data['image_3_delete_hash']
        if product_data['image_4_url'] != '':
            self.image_4_url = product_data['image_4_url']
        if product_data['image_4_delete_hash'] != '':
            self.image_4_delete_hash = product_data['image_4_delete_hash']
        if product_data['detail_1'] != '':
            self.detail_1 = product_data['detail_1']
        if product_data['detail_2'] != '':
            self.detail_2 = product_data['detail_2']
        if product_data['detail_3'] != '':
            self.detail_3 = product_data['detail_3']
        if product_data['detail_4'] != '':
            self.detail_4 = product_data['detail_4']
        if product_data['detail_5'] != '':
            self.detail_5 = product_data['detail_5']
        

class ProductSchema(ma.Schema):
    class Meta:
        fields = (  "id", "name", "price", "brand", "category_id",
                    "shop_id", "measurements", "description", "image_1_url", "image_2_url",
                    "image_3_url", "image_4_url",
                    "detail_1", "detail_2", "detail_3", "detail_4", "detail_5",
                    "created_by", "created_on")

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

import os
import jwt
from shared import db, ma
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta


class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    owns_shop = db.Column(db.String(3))
    address = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phonenumber = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())


    def __init__(self, user_obj):
        self.name = user_obj['name']
        self.owns_shop = user_obj['owns_shop']
        self.address = user_obj['address']
        self.email = user_obj['email']
        self.password = Bcrypt().generate_password_hash(user_obj['password']).decode()
        self.phonenumber = user_obj['phonenumber']
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def check_password(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def generate_token(self):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=360),
                'iat': datetime.utcnow(),
                'sub': self.id,
                'owns_shop': self.owns_shop
            }
            jwt_string = jwt.encode(
                payload,
                str(os.getenv('SECRET')),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            return str(e)

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "address", "email", "phonenumber")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

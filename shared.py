from flask_sqlalchemy import SQLAlchemy
from flask_api import FlaskAPI
from flask_marshmallow import Marshmallow

app = FlaskAPI(__name__)
db = SQLAlchemy()
ma = Marshmallow(app)
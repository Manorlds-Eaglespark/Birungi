import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.views import db, create_app
from app.models.product import Product
from app.models.category import Category
from app.models.amenities import Amenity
from app.models.photos import Photo
from app.models.users import User
from app.models.shops import Shop

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
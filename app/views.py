import os
import re
from flask import Flask
from flask_api import FlaskAPI
from flask_marshmallow import Marshmallow
from flask import Flask, request, jsonify, make_response, json
from datetime import datetime
from instance.config import app_config
from dotenv import load_dotenv
from flask_cors import CORS
from shared import db
from app.utilities.flask_imgur import Imgur
from app.models.shops import Shop, shop_schema, shops_schema
from app.models.product import Product, product_schema, products_schema
from app.models.category import Category, category_schema, categories_schema
from app.models.amenities import Amenity, amenities_schema, amenity_schema
from app.models.photos import Photo, photo_schema, photos_schema
from app.models.users import User, user_schema, users_schema
from app.utilities.model_validations import Register_Validation, Shop_Validation
from app.models.category import Category
from app.models.cart import Cart, cart_schema, carts_schema
from app.utilities.helpers import Helpers
from app.utilities.check_loggedin import login_required


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["IMGUR_ID"] = "0c78f4c5dd9bce4"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
    db.init_app(app)
    ma = Marshmallow(app)
    imgur_handler = Imgur(app)
    helper = Helpers()
    CORS(app)


    @app.route('/', methods=['GET'])
    def welcome_to_api():
        response = {"status": 200, "data": [{
            "message": "Welcome To Birungi API.",
                                            "endpoint 1": "GET     /api/v1/products - get all products",
                                            "endpoint 2": "GET     /api/v1/products/<product-id> - get one product",
                                            "endpoint 3": "POST    /api/v1/categories     - get all categories",
                                            "endpoint 4": "PUT   /api/v1/categories/<category-id>"
                                            }]
                    }
        return make_response(jsonify(response)), 200

# Shop Endpoints ############################################################################################################

    @app.route('/api/v1/shops', methods=['GET'])
    def get_shops():
        shops = Shop.query.all()
        return make_response(jsonify({'shops': shops_schema.dump(shops)})), 200

    @app.route('/api/v1/shops/<shop_id>', methods=['GET'])
    def get_shop(shop_id):
        shop = Shop.query.get(shop_id)
        if shop:
            return make_response(jsonify({'shop': shop_schema.dump(shop)})), 200
        else:
            return make_response(jsonify({"message": "Shop does not exist."})), 404

    @app.route('/api/v1/shops/owned', methods=['GET'])
    @login_required
    def get_owner_shop(current_user):
        shop = Shop.query.filter_by(owner=current_user).first()
        if shop:
            return make_response(jsonify({'shop': shop_schema.dump(shop)})), 200
        else:
            return make_response(jsonify({"message": "Shop does not exist."})), 404


    @app.route('/api/v1/shops/create', methods=['POST'])
    @login_required
    def create_new_shop(current_user):
        name = request.data.get('name', '')
        address = request.data.get('address', '')
        email = request.data.get('email', '')
        tel1 = request.data.get('tel1', '')
        tel2 = request.data.get('tel2', '')
        brief = request.data.get('brief', '')
        description = request.data.get('description', '')
        shop_data = {"name": name, "owner": current_user, "address": address, "email": email, "telephone_1": tel1, "telephone_2": tel2, "short_brief":brief, "description": description}
        validate_shop_data = Shop_Validation(shop_data)
        is_verified = validate_shop_data.check_input()
        if is_verified[0] == 200:
            shop = Shop(shop_data)
            if Shop.query.filter_by(email=email).first():
                return make_response(jsonify({"message":"Enter a different email address. Another business already uses that email."})), 400
            else:
                user = User.query.get(current_user)
                if int(user.owns_shop) == 1:
                    return make_response(jsonify({'error': 'Only primium users can have more than one shop.'})),401
                user.owns_shop = 1
                user.save()
                shop.save()
                return make_response(jsonify(
                    {"shop": shop_schema.dump(shop), "message": "Shop Successfully Added."})), 201
        else:
                return make_response(jsonify({"message":is_verified[1]})), is_verified[0]

    
    @app.route('/api/v1/shops/edit', methods=['GET','PUT', 'DELETE'])
    @login_required
    def edit_shop(current_user):
        shop = Shop.query.filter_by(owner=current_user).first()
        if request.method == 'GET':
            if shop:
                return make_response(jsonify({'shop': shop_schema.dump(shop)})), 200
            else:
                return make_response(jsonify({"message": "Shop does not exist."})), 404

        if request.method == 'PUT':
            input_data = request.data
            name = input_data.get('name', '')
            address = input_data.get('address', '')
            email = input_data.get('email', '')
            tel1 = input_data.get('tel1', '')
            tel2 = input_data.get('tel2', '')
            brief = input_data.get('brief', '')
            description = input_data.get('description', '')
            shop_data = {'name': name, 'address': address, 'email': email, 'telephone_1': tel1, 'telephone_2': tel2, 'brief': brief, 'description': description}
            shop.add_added(shop_data)
            shop.save()
            return make_response(jsonify({"message": "Shop successfully updated.", "shop": shop_schema.dump(shop)}))
        
        if request.method == 'DELETE':
            user = User.query.get(current_user)
            user.owns_shop = 0
            shop.delete()
            user.save()
            return make_response(jsonify({"message": "Shop successfully deleted."})), 202




# Category Crud Users ############################################################################################################

    @app.route('/api/v1/categories', methods=['GET'])
    def add_category():
        categories = Category.query.all()
        return make_response(jsonify({'categories': categories_schema.dump(categories)})), 200

    @app.route('/api/v1/categories/<category_id>', methods=['GET'])
    def get_edit_delete_category(category_id):
        category = Category.query.get(category_id)
        if category:
            return make_response(jsonify({'category': category_schema.dump(category)})), 200
        else:
            return make_response(jsonify({"message": "Category does not exist."})), 404

    @app.route('/api/v1/categories/<category_id>/products', methods=['GET'])
    def get_category_products(category_id):
            products = Product.query.filter_by(category_id=category_id).all()
            products_all = products_schema.dump(products)
            all_products = []
            for product in products_all:
                product['images'] = photos_schema.dump(Photo.query.filter_by(product_id=product['id']))
                product['amenities'] = amenities_schema.dump(Amenity.query.filter_by(product_id=product['id']))
                all_products.append(product)
            return make_response(jsonify({"products": all_products})), 200

# Product Crud User ############################################################################################################

    @app.route('/api/v1/products', methods=['GET'])
    def add_get_product():
            products = Product.query.all()
            products_all = products_schema.dump(products)
            return make_response(jsonify({"products": products_all})), 200

    @app.route('/api/v1/products/shop/<shop_id>', methods=['GET'])
    def get_shop_product(shop_id):
            products = Product.query.filter_by(shop_id=shop_id)
            products_all = products_schema.dump(products)
            return make_response(jsonify({"products": products_all})), 200

    @app.route('/api/v1/products/<product_id>', methods=['GET'])
    def get_edit_delete_product(product_id):
        product = Product.query.get(product_id)
        product = product_schema.dump(product)
        return make_response(jsonify({'product': product})), 200

    @app.route('/api/v1/products/search', methods=['POST'])
    def search_products_if_available():
        search_query = request.data.get('search', '')
        products_name = Product.query.filter(Product.name.ilike("%" + search_query + "%")).all()
        products_brand = Product.query.filter(Product.brand.ilike("%" + search_query + "%")).all()
        products_1 = products_schema.dump(products_name)
        products_2 = products_schema.dump(products_brand)
        products = helper.remove_dupes(products_1 + products_2)
        products_all = products_schema.dump(products)
        all_products = []
        for product in products_all:
            product['images'] = photos_schema.dump(Photo.query.filter_by(product_id=product['id']))
            product['amenities'] = amenities_schema.dump(Amenity.query.filter_by(product_id=product['id']))
            all_products.append(product)
        return make_response(jsonify({"products": all_products})), 200

# User endpoints ############################################################################################################

    @app.route('/api/v1/user/login', methods=['POST'])
    def login_user():
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                access_token = user.generate_token()
                return make_response(jsonify({"message":"You successfully logged-in.", "token": access_token.decode(), "shop_owner": user.owns_shop}))
            else:
                return make_response(jsonify({"message": "You entered a wrong password."})), 401
        else:
            return make_response(jsonify({"message": "You entered wrong credentials."})), 401
      
    @app.route('/api/v1/user/register', methods=['POST'])
    def register_new_user():
        name = request.data.get('name', '')
        address = request.data.get('address', '')
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        phonenumber = request.data.get('phonenumber', '')
        user_data = {"name": name, "owns_shop": 0, "address": address, "email": email, "password": password, "phonenumber": phonenumber}
        validate_user_data = Register_Validation(user_data)
        is_verified = validate_user_data.check_input()
        if is_verified[0] == 200:
            user = User(user_data)
            if User.query.filter_by(email=email).first():
                return make_response(jsonify({"message":"Enter a different email address. Someone already uses that email."})), 400
            else:
                user.save()
                return make_response(jsonify(
                    {"user": user_schema.dump(user), "message": "User Successfully Registered"})), 201
        else:
            return make_response(jsonify({"message":is_verified[1]})), is_verified[0]

    @app.route('/api/v1/users', methods=['GET'])
    @login_required
    def get_users(current_user):
        users = User.query.all()
        return users_schema.dumps(users)

# Cart Crud Endpoints ############################################################################################################
  
    @app.route('/api/v1/admin/carts', methods=['GET', 'POST'])
    @login_required
    def admin_add_cart(current_user):
        if request.method == 'POST':
            item_list = request.form.get('item_list', '')
            item_qty = request.form.get('item_qty', '')
            status = 'new'
            cart_data = {'item_list': item_list, 'item_qty': item_qty, 'created_by': current_user}
            if not (item_list and item_qty):
                return make_response(jsonify({}))
            # process cart order details and send notifications
            cart = Cart(cart_data)
            cart.save()
            return make_response(jsonify({'cart': cart_schema.dump(cart), 'message': 'Order successfully received.'})), 201
        if request.method == 'GET':
            carts_all = Cart.query.all()
            return make_response(jsonify({'carts': carts_schema.dumps(carts_all)}))
    
    @app.route('/api/v1/admin/carts/<cart_id>', methods=['GET', 'PUT', 'DELETE'])
    @login_required
    def admin_get_edit_delete_cart(current_user, cart_id):
        cart = Cart.query.get(cart_id)
        if cart:
            if request.method == 'GET':
                return make_response(jsonify({'cart': cart_schema.dumps(cart)}))
            if request.method == 'DELETE':
                cart.delete()
                return make_response(jsonify({'message': 'Cart successfully deleted.'}))
            if request.method == 'PUT':
                status = request.form.get('status', '')
                cart.add_added(status)
                cart.save()
                return make_response(jsonify({'cart': cart_schema.dumps(cart), 'message': 'Cart successfully updated.'}))

        else:
            return make_response(jsonify({'message': 'Cart not found.'}))
        

# Category Crud Admin ############################################################################################################

    @app.route('/api/v1/admin/categories', methods=['GET', 'POST'])
    @login_required
    def admin_add_category(current_user):
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            image = request.files['icon_file']
            image_data = imgur_handler.send_image(image)
            icon_url = image_data["data"]["link"]
            icon_delete_hash =  image_data["data"]["deletehash"]
            category_data = {'name': name, 'description': description, 'icon_url': icon_url, 'icon_delete_hash': icon_delete_hash, 'created_by': current_user}
            category = Category(category_data)
            category.save()
            return make_response(jsonify({'category': category_schema.dump(category), 'message': 'new category successfully added.'})), 201
        
        elif request.method == 'GET':
            categories = Category.query.all()
            return make_response(jsonify({'categories': categories_schema.dump(categories)})), 200

    @app.route('/api/v1/admin/categories/<category_id>', methods=['GET', 'PUT', 'DELETE'])
    @login_required
    def admin_get_edit_delete_category(current_user, category_id):
        category = Category.query.get(category_id)
        if category:
            if request.method == 'GET':
                return make_response(jsonify({'category': category_schema.dump(category)})), 200
            elif request.method == 'PUT':
                name = request.form.get('name', '')
                description = request.form.get('description', '')
                icon_url = request.form.get('icon_url', '')
                category_data = {'name': name, 'description': description, 'icon_url': icon_url}
                category.add_added(category_data)
                category.save()
                return make_response(jsonify({"message": "Category detail successfully updated.", "category": category_schema.dump(category)})),202
            elif request.method == 'DELETE':
                imgur_handler.delete_image(delete_hash=category.icon_delete_hash)
                category.delete()
                return make_response(jsonify({"message": "You successfully deleted a product category with Id "+ str(category.id)})), 200
        else:
            return make_response(jsonify({"message": "Category does not exist."})), 404

    @app.route('/api/v1/admin/categories/<category_id>/products', methods=['GET', 'POST'])
    @login_required
    def admin_get_category_products(current_user, category_id):
        if request.method == 'GET':
            products = Product.query.filter_by(category_id=category_id).all()
            products_all = products_schema.dump(products)
            return make_response(jsonify({"products": products_all})), 200


# Product Crud Admin ############################################################################################################

    @app.route('/api/v1/admin/products', methods=['GET', 'POST'])
    @login_required
    def admin_add_get_product(current_user):    
        if request.method == 'GET':
            products = Product.query.all()
            products_all = products_schema.dump(products)
            return make_response(jsonify({"products": products_all})), 200

        elif request.method == 'POST':
            name = request.form.get('name', '')
            price = request.form.get('price', '')
            brand = request.form.get('brand','')
            measurements = request.form.get('measurements', '')
            description = request.form.get('description', '')
            category_id = int(request.form.get('category_id', ''))
            shop_id = int(request.form.get('shop_id', ''))
            image_1 = request.files['image_1']
            if image_1:
                image_1_data = imgur_handler.send_image(image_1)
                image_1_url = image_1_data["data"]["link"]
                image_1_delete_hash =  image_1_data["data"]["deletehash"]
            else:
                image_1_url = ''
                image_1_delete_hash = ''

            image_2 = request.files['image_2']
            if image_2:
                image_2_data = imgur_handler.send_image(image_2)
                image_2_url = image_2_data["data"]["link"]
                image_2_delete_hash =  image_2_data["data"]["deletehash"]
            else:
                image_2_url = ''
                image_2_delete_hash = ''

            image_3 = request.files['image_3']
            if image_3:
                image_3_data = imgur_handler.send_image(image_3)
                image_3_url = image_3_data["data"]["link"]
                image_3_delete_hash =  image_3_data["data"]["deletehash"]
            else:
                image_3_url = ''
                image_3_delete_hash = ''

            image_4 = request.files['image_4']
            if image_4:
                image_4_data = imgur_handler.send_image(image_4)
                image_4_url = image_1_data["data"]["link"]
                image_4_delete_hash =  image_1_data["data"]["deletehash"]
            else:
                image_4_url = ''
                image_4_delete_hash = ''

            detail_1 = request.form.get('detail_1', '')
            detail_2 = request.form.get('detail_2', '')
            detail_3 = request.form.get('detail_3', '')
            detail_4 = request.form.get('detail_4', '')
            detail_5 = request.form.get('detail_5', '')

            product_data = {'name': name, 'price': price, 'brand': brand, 'category_id': category_id, 'description': description, 'shop_id': shop_id, 'measurements': measurements,
                'image_1_url': image_1_url, 'image_1_delete_hash': image_1_delete_hash, 'image_2_url': image_2_url, 'image_2_delete_hash': image_2_delete_hash,
                'image_3_url': image_3_url, 'image_3_delete_hash': image_3_delete_hash, 'image_4_url': image_4_url, 'image_4_delete_hash': image_4_delete_hash,
                'detail_1': detail_1, 'detail_2': detail_2, 'detail_3': detail_3,
                'detail_4': detail_4, 'detail_5': detail_5, 'created_by': current_user}
            product = Product(product_data)
            product.save()
            return make_response(jsonify({'product': product_schema.dump(product), 'message': 'Product successfully added.'})), 201
        

    @app.route('/api/v1/admin/products/<product_id>', methods=['GET', 'PUT', 'DELETE'])
    @login_required
    def admin_get_edit_delete_product(current_user, product_id):
        product = Product.query.get(product_id)
        if product:
            if request.method == 'GET':
                product = product_schema.dump(product)
                return make_response(jsonify({'product': product})), 200

            elif request.method == 'PUT':
                name = request.form.get('name', '')
                brand = request.form.get('brand', '')
                price = request.form.get('price', '')
                measurements = request.form.get('measurements', '')
                description = request.form.get('description', '')
                detail_1 = request.form.get('detail_1', '')
                detail_2 = request.form.get('detail_2', '')
                detail_3 = request.form.get('detail_3', '')
                detail_4 = request.form.get('detail_4', '')
                detail_5 = request.form.get('detail_5', '')
                image_1_url = request.form.get('image_1_url', '')
                image_1_delete_hash = request.form.get('image_1_delete_hash', '')
                image_2_url = request.form.get('image_2_url', '')
                image_2_delete_hash = request.form.get('image_2_delete_hash', '')
                image_3_url = request.form.get('image_3_url', '')
                image_3_delete_hash = request.form.get('image_3_delete_hash', '')
                image_4_url = request.form.get('image_4_url', '')
                image_4_delete_hash = request.form.get('image_4_delete_hash', '')

                product_data = {'name': name, 'price': price, 'brand': brand, 'measurements': measurements, 
                                'description': description, 'detail_1': detail_1, 'detail_2': detail_2, 'detail_3': detail_3, 
                                'detail_4': detail_4, 'detail_5': detail_5, 'image_1_delete_hash':image_1_delete_hash, 
                                'image_2_delete_hash':image_2_delete_hash, 'image_3_delete_hash':image_3_delete_hash, 
                                'image_4_delete_hash':image_4_delete_hash,
                                'image_1_url':image_1_url, 'image_2_url':image_2_url, 'image_3_url':image_3_url, 'image_4_url':image_4_url}
                product.add_added_detail(product_data)
                product.save()
                return make_response(jsonify({"message": "Product successfully updated.", "product": product_schema.dump(product)}))
            
            elif request.method == 'DELETE':
                imgur_handler.delete_image(delete_hash=product.image_1_delete_hash)
                imgur_handler.delete_image(delete_hash=product.image_2_delete_hash)
                imgur_handler.delete_image(delete_hash=product.image_3_delete_hash)
                imgur_handler.delete_image(delete_hash=product.image_4_delete_hash)
                product.delete()
                return make_response(jsonify({'message': 'You successfully deleted a product with Id '+str(product.id)})), 200
        else:
            return make_response(jsonify({"message": "Product does not exist."})), 404

    @app.route('/api/v1/admin/products/search', methods=['POST'])
    @login_required
    def admin_search_products_if_available(current_user):
        search_query = request.data.get('search', '')
        products_name = Product.query.filter(Product.name.ilike("%" + search_query + "%")).all()
        products_brand = Product.query.filter(Product.brand.ilike("%" + search_query + "%")).all()
        products_1 = products_schema.dump(products_name)
        products_2 = products_schema.dump(products_brand)
        products = helper.remove_dupes(products_1 + products_2)
        products_all = products_schema.dump(products)
        return make_response(jsonify({"products": products_all})), 200


    return app

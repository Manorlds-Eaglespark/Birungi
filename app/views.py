import os
import re
from flask_api import FlaskAPI
from flask_marshmallow import Marshmallow
from flask import Flask, request, jsonify, make_response, json
from datetime import datetime
from instance.config import app_config
from dotenv import load_dotenv
from flask_cors import CORS
from shared import db
from sqlalchemy_searchable import search
from app.models.product import Product, product_schema, products_schema
from app.models.category import Category
from app.utilities.helpers import Helpers


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
    db.init_app(app)
    ma = Marshmallow(app)
    CORS(app)


    @app.route('/', methods=['GET'])
    def welcome_to_api():
        response = {"status": 200, "data": [{
            "message": "Welcome To Birungi API.",
                                            "endpoint 1": "GET     /api/v1/products - get all products",
                                            "endpoint 2": "GET     /api/v1/products/<product-id> - get one product",
                                            "endpoint 3": "POST    /api/v1/categories     - get all categories",
                                            "endpoint 4": "PATCH   /api/v1/categories/<category-id>"
                                            }]
                    }
        return make_response(jsonify(response)), 200

# Product Crud ######################################################

    @app.route('/api/v1/products', methods=['POST'])
    def add_product():
        if request.method == 'POST':
            input_data = request.data
            name = input_data.get('name', '')
            price = input_data.get('price', '')
            brand = input_data.get('brand', '')
            category = input_data.get('category', '')
            description = input_data.get('description', '')
            dimensions = input_data.get('dimensions', '')
            product_data = {'name': name, 'price': price, 'brand': brand, 'category': category, 'description': description, 'dimensions': dimensions}
            product = Product(product_data)
            product.save()
            return make_response(jsonify({'product': product_schema.dump(product), 'message': 'new product added.'})), 201
        
        if request.method == 'GET':
            products = Product.query.all()
            return make_response(jsonify({'products': products_schema.dump(products)})), 200

    @app.route('/api/v1/products/<product_id>', methods=['GET', 'PUT', 'DELETE'])
    def get_edit_delete_product(product_id):
        product = Product.query.get(product_id)
        if request.method == 'GET':
            return make_response(jsonify({'product': product_schema.dump(product)})), 200
        elif request.method == 'PUT':
            input_data = request.data
            name = input_data.get('name', '')
            price = input_data.get('price', '')
            brand = input_data.get('brand', '')
            category = input_data.get('category', '')
            description = input_data.get('description', '')
            dimensions = input_data.get('dimensions', '')
            product_data = {'name': name, 'price': price, 'brand': brand, 'category': category, 'description': description, 'dimensions': dimensions}
            product.add_added(product_data)
            product.save()
        elif request.method == 'DELETE':
            product.delete()
            return make_response(jsonify({'message': 'You successfully deleted a product with Id '+product.id})), 200
      
# Search product ############################################################

    @app.route('/api/v1/products/search', methods=['POST'])
    def search_products_if_available():
        search_query = request.data.get('search_term', '')
        products = search(Product.query, search_query)
        # products = Product.query.filter(Product.name.like('%' + search_term + '%')).all()
        return make_response(jsonify({"products": products_schema.dump(products)})), 200

# Add Product Category ########################################################

    @app.route('/api/admin/v1/categories', methods=['GET','POST'])
    def add_category():
        if request.method == 'POST':
            input_data = json.loads(request.data)
            name = input_data['name']
            description = input_data['description']
            icon_image = input_data['icon_image']
            category = Category(name, description, icon_image)
            saved_category = database.save_new_category(category)
            return make_response(jsonify({"status": "201 OK", "Category": Helpers.convert_array_to_JSON_category(saved_category)}))

        if request.method == 'GET':
            categories = database.get_all_categories()
            return make_response(jsonify({"status": "200 OK", "category_count": len(categories), "data": categories }))

# Fetch All Product Categories ######################################################
    @app.route('/api/v1/products/categories', methods=['GET'])
    def get_all_categories():
        categories = database.get_all_categories()
        return make_response(jsonify({"status": "200 OK", "category_count": len(categories),"categories": Helpers.convert_category_array_to_JSON(categories)})), 200


# Fetch product Category ######################################################
    @app.route('/api/v1/products/categories/<category_id>', methods=['GET'])
    def get_all_products_in_category(category_id):
        products = database.get_products_category(category_id)
        return make_response(jsonify({"status": "200 OK", "product_count":len(products) , "products": Helpers.convert_array_to_JSON_many_products(products)}))


# CRUD product ################################################################



# Test app gateway #################################################################   

    @app.route('/api/v1/pools', methods=['GET'])
    def get_pool_products():
        products = database.get_products()
        return make_response(jsonify({"data":"this is some data"})), 500

    return app

from ecom_app import app, db, User, Order, Product, user_schema, product_schema, order_schema, users_schema, products_schema, orders_schema
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from sqlalchemy import ForeignKey, Table, String, Column, DateTime, select, create_engine, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional

#MARK: Users
# Retrive all users(SUCCESSFUL-200)
@app.route('/users', methods = ['GET'])
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all() 

    return users_schema.jsonify(users), 200  
           
#GET /users/<id>: Retrieve a user by ID (SUCCESSFUL-200)
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)
    return user_schema.jsonify(user), 200
 
#POST /users: Create a new user (SUCCESSFUL-200)
@app.route('/users', methods = ['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
    
        return jsonify(e.messsages), 400
    
    new_user = User(name=user_data['name'], address=user_data['address'], email=user_data['email'])
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201

#PUT /users/<id>: Update a user by ID (SUCCESSFUL-200)
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.get(User,id)

    if not user:
        return jsonify({"message":"User Not Found!"}), 400
    
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    user.name = user_data['name']
    user.email = user_data['email']

    db.session.commit()
    return user_schema.jsonify(user), 200



#DELETE /users/<id>: Delete a user by ID(SUCCESSFUL-200)
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User,id)

    if not user:
         return jsonify({"message": "User Not Found!"}), 400
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"successfully deleted {user.name}"}), 200


#MARK: Products
# Product Endpoints
# GET /products: Retrieve all products (SUCCESSFUL-200)
@app.route('/products', methods = ['GET'])
def get_all_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all() 

    return products_schema.jsonify(products), 200  

# GET /products/<id>: Retrieve a product by ID (SUCCESSFUL-200)
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = db.session.get(Product, id)
    return product_schema.jsonify(product), 200

# POST /products: Create a new product (SUCCESSFUL-200)
@app.route('/product', methods = ['POST'])
def create_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_product = Product(product_name=product_data['product_name'], price=product_data['price'])
    db.session.add(new_product)
    db.session.commit()
    return user_schema.jsonify(new_product), 201



# PUT /products/<id>: Update a product by ID (SUCCESSFUL-200)
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = db.session.get(Product, id)

    if not product:
        return jsonify({"message":"Invalid product id"}), 400
    
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    product.product_name = product_data['product_name']
    product.price = product_data['price']

    db.session.commit()
    return product_schema.jsonify(product), 200
print("user has been updated!") 

# DELETE /products/<id>: Delete a product by ID (SUCCESSFUL-200)
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_products(id):
    product = db.session.get(Product,id)

    if not product:
         return jsonify({"message": "Product Not Found!"}), 400
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"successfully deleted {product.product_name}"}), 200


#MARK: Orders
# Order Endpoints
# POST /orders: Create a new order (requires user ID and order date)#(Still working on this)
@app.route('/orders/<int:id>', methods=['POST']) 
def create_order(id):
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages),400

    new_order = Order(user_id=order_data['user_id'], order_date=order_data['order_date'])
    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify(new_order), 200


# POST /orders/<order_id>/add_product/<product_id>: Add a product to an order (prevent duplicates)
@app.route('/orders/<order_id>/add_product/<product_id>', methods=['POST'])
def add_product(order_id, product_id):
    order = db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)

    order.products.append(product)
    db.session.commit()

# # DELETE /orders/<order_id>/remove_product/<product_id>: Remove a product from an order
@app.route('/orders/<order_id>/remove_product/<product_id>', methods=['DELETE'])
def remove_product(order_id, product_id):
    order = db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)
    
    if not product and order:
         return jsonify({"message": "Product Not Found!"}), 400
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"successfully deleted {product.product_name}"}), 200

# GET /orders/user/<user_id>: Get all orders for a user
@app.route('/order/user/<user_id>', methods = ['GET'])
def get_orders(id):
    query = select(Order, id)
    orders = db.session.execute(query).scalars().all()
    return order_schema.jsonify(orders), 200


# GET /orders/<order_id>/products: Get all products for an order
@app.route('/orders/<order_id>/products', methods=['GET'])
def get_order_products(id):
    query = select(Product, id)
    products = db.session.execute(query).scalars().all()

    return products_schema.jsonify(products), 200  

app.run(debug=True)
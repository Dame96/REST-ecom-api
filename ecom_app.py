# importing all modules/libraries needed
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields 
from sqlalchemy import ForeignKey, Table, String, Column, DateTime, func, create_engine, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional

#creating a flask app
 
app = Flask(__name__)
CORS(app)

# Database config - establishing link to db in workbench. 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Dametech1!@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Base class, other classes inherit from. 
class Base(DeclarativeBase):
    pass

#Initialize SQLAlchemy and Marshmallow 
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)

# Association table order product. 

order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", ForeignKey("orders.order_id", ondelete="CASCADE"), primary_key=True),
    Column("product_id", ForeignKey("products.product_id", ondelete="CASCADE"),primary_key=True),
)


#creating user class, inherits from "Base"
class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    address: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(40), unique=True)
    
    #One to many relationship
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user")

    
class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    order_date : Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))

    #relationship attribute 
    # links one user to an order 
    user: Mapped["User"] = relationship("User", back_populates="orders")

    # One to many relationship
    products: Mapped[List["Product"]] = relationship(secondary=order_product, back_populates="orders")

class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(25))
    price: Mapped[float]
    
    # One product can be connected to several different orders 
    orders: Mapped[List["Order"]] = relationship(secondary=order_product, back_populates="products")

# creating schemas for validation of json data that comes in via request

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
    user_id = fields.Integer()

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product 



user_schema = UserSchema()
order_schema = OrderSchema()
product_schema = ProductSchema()

users_schema = UserSchema(many=True)
orders_schema = OrderSchema(many=True)
products_schema = ProductSchema(many=True)


if __name__=="_main__":
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)









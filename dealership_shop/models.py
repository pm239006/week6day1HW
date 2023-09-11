from werkzeug.security import generate_password_hash 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin, LoginManager 
from datetime import datetime
import uuid 
from flask_marshmallow import Marshmallow
from .helpers import get_image


db = SQLAlchemy() 
login_manager = LoginManager() 
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) 

class User(db.Model,UserMixin):
    user_id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30))
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self,username,email,password, first_name= "", last_name = ""):
        self.user_id = self.set_id() #method to create unique id 
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = self.set_password(password) #method to hash our password for security 

    def set_id(self):
        return str(uuid.uuid4()) #random username - unique user id 
    def get_id(self):
        return str(self.user_id)

    def set_password(self,password):
        return generate_password_hash(password)
    
    def __repr__(self):
        return f"USER: {self.username}"
    
class Product(db.Model):
    prod_id = db.Column(db.String, primary_key = True)
    car_model = db.Column(db.String(100), nullable = False)
    car_make = db.Column(db.String(100), nullable = False)
    car_year = db.Column(db.String(100), nullable = False)
    image = db.Column(db.String, nullable = False)
    description = db.Column(db.String(200))
    price = db.Column(db.Numeric(precision=10, scale=2), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    #user_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable = False) #if we wanted to make a foreign key relationship


    def __init__(self, car_make, car_model, car_year, price, quantity, image = "", description = ""):
        self.prod_id = self.set_id()
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.price = price
        self.quantity = quantity
        self.image = self.set_image(image, car_make)
        self.description = description

    def set_id(self):
        return str(uuid.uuid4()) 
    
    def set_image(self, image, car_make, car_model, car_year):
        if not image:
            image = get_image(car_make, car_model, car_year)
            print("api image", image)

        return image
    
    def decrement_quantity(self, quantity):

        self.quantity -= int(quantity)
        return self.quantity #all methods need to return otherwise the object attribute doesnt get updated
    
    def increment_quantity(self, quantity):

        self.quantity += int(quantity)
        return self.quantity
    

    def __repr__(self):
        return f"<PRODUCT: {self.name}>"



class Customer(db.Model):
    cust_id = db.Column(db.String, primary_key = True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    prodord  = db.relationship('ProdOrder', backref = 'customer', lazy = True) 


    def __init__(self, cust_id):
        self.cust_id = cust_id



class ProdOrder(db.Model):
    prodorder_id = db.Column(db.String, primary_key = True)
    prod_id = db.Column(db.String, db.ForeignKey('product.prod_id'), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Numeric(precision = 10, scale = 2), nullable = False)
    order_id = db.Column(db.String,  db.ForeignKey('order.order_id'), nullable = False)
    cust_id = db.Column(db.String, db.ForeignKey('customer.cust_id'), nullable = False)


    def __init__(self, prod_id, quantity, price, order_id, cust_id):
        self.prodorder_id = self.set_id()
        self.prod_id = prod_id
        self.quantity = quantity
        self.price = self.set_price(price, quantity)
        self.order_id = order_id
        self.cust_id = cust_id 

    def set_id(self):
        return str(uuid.uuid4())


    def set_price(self, price, quantity):

        quantity = float(quantity)
        price = float(price)

        self.price = quantity * price
        return self.price 
    

    def update_quantity(self, quantity): #method used for when customers update their order quantity of a specific product 

        self.quantity = int(quantity)
        return self.quantity
    


class Order(db.Model):
    order_id = db.Column(db.String, primary_key = True)
    order_total = db.Column(db.Numeric(precision = 10, scale = 2), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    prodorder = db.relationship('ProdOrder', backref = 'order', lazy = True)


    def __init__(self):
        self.order_id = self.set_id()
        self.order_total = 0.00


    def set_id(self):
        return str(uuid.uuid4())
    

    #for every product's total price in prodorder table add to our order's total price 
    def increment_order_total(self, price):

        self.order_total = float(self.order_total)
        self.order_total += float(price)

        return self.order_total
    
    def decrement_order_total(self, price):

        self.order_total = float(self.order_total)
        self.order_total -= float(price)


        return self.order_total 
    
    def __repr__(self):

        return f"<ORDER: {self.order_id}>"
    

#Because we are building a RESTful API this week (Representational State Transfer) 
#json rules that world. JavaScript Object Notation aka dictionaries 


# #Build our Schema
# #How your object looks when being passed from server to server 
# #These will look like dictionaries 

class ProductSchema(ma.Schema):
    class Meta: 
        fields = ['car_make', 'car_model', 'car_year', 'name', 'image', 'description', 'price', 'quantity'] 



product_schema = ProductSchema() #this is for passing 1 singular product 
products_schema = ProductSchema(many = True) #this for passing multiple products, list of dictionaries 
    
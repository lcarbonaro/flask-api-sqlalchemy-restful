# imports
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

# initialise flask app
app = Flask(__name__)

# app db config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# models
class Product(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)  
    desc = db.Column(db.String(50))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    reviews = db.relationship('Review', backref='product')

    # don't forget that every tuple needs at least one comma!
    serialize_rules = ('-reviews.product',)

class Buyer(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)    
    reviews = db.relationship('Review', backref='buyer')

    # don't forget that every tuple needs at least one comma!
    serialize_rules = ('-reviews.buyer',)    

class Review(db.Model, SerializerMixin):    
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200))    
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'))

    serialize_rules = ('-product.reviews', '-buyer.reviews') ##critical??YES!!

# buyer buys many products
# products are bought by many buyers
# so many-to-many needs join table
# how used??
buyer_product = db.Table('buyer_product',
    db.Column('buyer_id', db.Integer, db.ForeignKey('buyer.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)


# test route
@app.route('/test', methods=['GET'])
def test():
    return {"hello": "work world"}

# add a product
# to-do: get fields from request, not hard-coded
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    desc = request.json['desc']
    price = request.json['price']
    qty = request.json['qty']
    new_product = Product(name,desc,price,qty)
    db.session.add(new_product)
    db.session.commit()
    return new_product.to_dict()

# get all products
@app.route('/product', methods=['GET'])
def get_products():
  all_products = Product.query.all()  
  return [product.to_dict() for product in all_products]  # note 'list comprehension'


# get product by id
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product.to_dict()


# get all buyers
@app.route('/buyer', methods=['GET'])
def get_buyers():
  all_buyers = Buyer.query.all()  

  # note: can put rules here too, e.g. to leave out reviews: rules=('-reviews',)
  return [buyer.to_dict() for buyer in all_buyers] # note 'list comprehension'


# get buyer by id
@app.route('/buyer/<id>', methods=['GET'])
def get_buyer(id):
  buyer = Buyer.query.get(id)

  # note: can put rules here too, e.g. to leave out product: rules=('-reviews.product',)
  return buyer.to_dict()




# start flask server
if __name__ == '__main__':
    app.run(debug=True)

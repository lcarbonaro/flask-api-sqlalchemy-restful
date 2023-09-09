# imports
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_restful import Resource, Api 

# initialise flask app
app = Flask(__name__)

# app db config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# model classes
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

# resource classes
class ProductResource(Resource):
  def get(self, id=None):
    if not id:
      all_products = Product.query.all()  
      return [product.to_dict() for product in all_products]  # note 'list comprehension'
    else:  
      product = Product.query.get(id)
      return product.to_dict()

  def post(self):    
    desc = request.json['desc']
    price = request.json['price']
    qty = request.json['qty']
    new_product = Product(desc=desc,price=price,qty=qty)
    db.session.add(new_product)
    db.session.commit()
    return new_product.to_dict()

  def delete(self, id):
    del_product = Product.query.get(id)
    db.session.delete(del_product)
    db.session.commit()
    return del_product.to_dict()

  def put(self, id):
    product = Product.query.get(id)
    desc = request.json['desc']
    price = request.json['price']
    qty = request.json['qty']
    product.desc = desc
    product.price = price
    product.qty = qty
    db.session.commit()
    return product.to_dict()

class BuyerResource(Resource):
  def get(self, id=None):
    if not id:
      all_buyers = Buyer.query.all()  
      return [buyer.to_dict() for buyer in all_buyers]  # note 'list comprehension'
    else:  
      buyer = Buyer.query.get(id)
      return buyer.to_dict()

  def post(self):    
    name = request.json['name']    
    new_buyer = Buyer(name=name)
    db.session.add(new_buyer)
    db.session.commit()
    return new_buyer.to_dict()

  def delete(self, id):
    del_buyer = Buyer.query.get(id)
    db.session.delete(del_buyer)
    db.session.commit()
    return del_buyer.to_dict()

  def put(self, id):
    buyer = Buyer.query.get(id)
    name = request.json['name']    
    buyer.name = name    
    db.session.commit()
    return buyer.to_dict()

class ReviewResource(Resource):
  def get(self, prod_id=None):
    if prod_id:
      all_reviews = Review.query.filter_by(product_id=prod_id)
      return [review.to_dict( rules=('-product',) ) for review in all_reviews]

  def post(self):
    comment  = request.json['comment']
    prod_id  = request.json['prod_id']
    buyer_id = request.json['buyer_id']
    new_review = Review(comment=comment,product_id=prod_id,buyer_id=buyer_id)
    db.session.add(new_review)
    db.session.commit()
    return new_review.to_dict()

'''
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
'''

api.add_resource(ProductResource, '/product','/product/<id>')
api.add_resource(BuyerResource,   '/buyer',  '/buyer/<id>'  )
api.add_resource(ReviewResource,  '/review',  '/review/<prod_id>' )

# start flask server
if __name__ == '__main__':
    app.run(debug=True)

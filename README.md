project folder:

mkdir my-flask-app-name
cd my-flask-app-name


checks:

`python --version` should give version 3, for example 3.9.13
`pip --version`
`pipenv --version`  if need be: pip install pipenv

set-up:

make sure you're in the project folder
`pipenv shell`    creates a pipfile in the project folder
`pipenv install flask flask-sqlalchemy sqlalchemy-serializer flask-restful`
new file app.py

code sections:
- # imports
- # initialise flask app
- # start flask server

start server with `python app.py` or `flask run`

code section:

- # test route

test the test route with postman

code section:

- # app db config

code section:

- # models
- start with 3 simple classes (just fields)
- Product, Buyer, Review

command line:

`flask shell`
`from app import db,Product,Buyer,Review`
`db.create_all()`   to create actual db tables

still from flask shell show how to create records:
`p = Product(desc="thing one",price=1.23,qty=44)`
`db.session.add(p)`
`db.session.commit()`
`b1 = Buyer(name="Tom")`
`b2 = Buyer(name="Jane")`
`db.session.add_all([b1,b2])`
`db.session.commit()`


add `SerializerMixin` to classes

code sections:

- # get all products
- # get all buyers

re-start server with `python app.py` or `flask run`

See https://thepythoncode.com/article/create-a-restful-api-with-flask-in-python

1. `from flask_restful import Resource, Api` 

2. `api = Api(app)`

3. code the resource classes
    - one resource class for each entity, 
    - and a `get` and `post` method in each resource class
    - not to be confused with model classes
        - so different names, for example:
            - model class is `Product` 
            - resource class is `ProductResource`

4. `api.add_resource(MyResourceClass, '/resource')`

5. move the various routes logic into `get` , `post` methods of each resource class



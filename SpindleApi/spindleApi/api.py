import markdown
import os
import json
from datetime import datetime

# Import the framework
from flask import Flask, g, request
from flask_restful import Resource, Api, reqparse

# Import Database
import pymongo

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

user = os.getenv('DB_USER')
password = os.environ.get('DB_PASSWORD')

# get dbClient and db
dbClient = pymongo.MongoClient(f'mongodb://{user}:{password}@mongo:27017/')
db = dbClient["spindleDb"]

def get_col(colname) :
    return db[colname]


@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


class SpindleList(Resource):
    def get(self):              
        result = db.list_collection_names()
        app.logger.debug(result)

        return {'message': 'Success', 'data': result}, 200  

class Spindle(Resource):
    def get(self, identifier):
        if(identifier not in db.list_collection_names()) :
            return {'message':"Spindle not found", 'data':{}}, 404
        
        col = get_col(identifier)
        result = col.find({}, {'_id': False}).sort('datetime',-1)[0]
        result['identifier'] = identifier
        app.logger.debug(result)
        
        return {'message': 'Success', 'data': result}, 200

    def post(self, identifier):
        data = request.data
        app.logger.info(data)
        loaded = json.loads(data)
        app.logger.info(loaded)
        loaded['datetime'] = datetime.now().isoformat()

        col = get_col(identifier)
        x = col.insert_one(loaded)


        return {'message': 'Success', 'data': f'{x.inserted_id}'}, 201

    def delete(self, identifier):
        # If the key does not exist in the data store, return a 404 error.
        if(identifier not in db.list_collection_names()) :
            return {'message':"Spindle not found", 'data':{}}, 404

        col = get_col(identifier)
        col.drop()

        return {'message': 'Success', 'data': {}}, 204

class SpindleData(Resource):
    def get(self, identifier):
        if(identifier not in db.list_collection_names()) :
            return {'message':"Spindle not found", 'data':{}}, 404

        col = get_col(identifier)
        result = col.find({}, {'_id': False}).sort('datetime',-1)
        return {'message': 'Success', 'data': list(result)}, 200



api.add_resource(SpindleList, '/spindles')
api.add_resource(Spindle, '/spindle/<string:identifier>')

api.add_resource(SpindleData, '/spindle/<string:identifier>/data')
 
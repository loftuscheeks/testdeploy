from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 201
        return {"message": "store is not found"}, 404
    
    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "A store with name '{}' is not found". format(name)}
        store = StoreModel(name)
        try:
            store.save_to_db()
            return {"message": "Store added successfully"}
        except:
            return {"message": "An error occurred"}
    
    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {"message": "Store does not exist, cannot delete the store"}, 400
        try:
            store.delete_from_db()
            return{"message": "Store deleted successfully"}, 201
        except:
            return{"message": "An error occurred"}, 500
    
    
class StoreList(Resource):
    
    @jwt_required()
    def get(self):
        return {"Stores": [store.json() for store in StoreModel.query.all() ]}
        
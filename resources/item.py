from flask_jwt import jwt_required
from flask_restful import Api, reqparse, Resource
from models.item import ItemModel

class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                            type=float,
                            required=True,
                            help="This field can not be left empty")
    parser.add_argument('store_id',
                            type=int,
                            required=True,
                            help="Every item needs a store id")
        
    @jwt_required()
    def get(self, name):
       
       item = ItemModel.find_by_name(name)
       if item:
           return item.json(), 201
       
       
       return {"message": "Item does not exist"}, 404
       
    
    @jwt_required()
    def post(self, name): 
        if ItemModel.find_by_name(name):
            return {'message': "An item with the name '{}' already exist".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred"}
        return {"message": "Item created successfully"}, 201
    
    @jwt_required()
    def put(self, name):  
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            
        item.save_to_db()
        return item.json(), 201
    
    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if ItemModel.find_by_name(name):
            item.delete_from_db()
            return {"message": "item '{}' deleted".format(name)}, 201
        return {"message": "item with the name '{}' not found, cannot delete".format(name)}, 404
        
    
class ItemList(Resource):
    
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
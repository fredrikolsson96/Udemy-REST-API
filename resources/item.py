from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    # create request parser
    parser = reqparse.RequestParser()
    # add the price and store-id as arguments to the request parser
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank'
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='Every item needs a store id'
    )
        
    # GET /item/<string:name>
    @jwt_required()
    def get(self, name):
        try:
            # retrieve the item, by name, from the database
            item = ItemModel.find_by_name(name)
        except:
            return {'An error occurred searching for the item'}, 500    # 500: internal server error

        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    # POST /item/<string:name>
    def post(self, name):
        # check if an item with that name already exists
        if ItemModel.find_by_name(name):
            return {'message': 'An item with name {} already exists'.format(name)}, 400

        # get only the parser arguments from the JSON payload
        data = Item.parser.parse_args()
        
        item = ItemModel(name, data.get('price'), data.get('store_id'))

        try:
            # save the item to the database
            item.save_to_db()
        except:
            return {'message': 'An error occurred saving to the database'}, 500    

        return item.json(), 201

    # DELETE /item/<string:name>
    def delete(self, name):
        try:
            item = ItemModel.find_by_name(name)
            if item:
                item.delete_from_db()
        except:
            return {'An error occurred deleting the item'}, 500

        return {'message': 'Item deleted'}

    # PUT /item/<string:name>
    def put(self, name):
        # get only the parser arguments from the JSON payload
        data = Item.parser.parse_args()

        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'An error occurred searching for the item'}, 500

        if item is None:
            item = ItemModel(name, data.get('price'), data.get('store_id'))
        else:
            item.price = data.get('price')
            item.store_id = data.get('store_id')

        try:
            item.save_to_db()
        except:
            return {'An error occurred while saving to the database'}, 500
    
        return item.json()


class ItemList(Resource):
    # GET /items
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
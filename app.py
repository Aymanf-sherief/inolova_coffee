import pymongo
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

MONGODB_URI = "mongodb+srv://ayman:<password>@cluster0-979xj.mongodb.net/inolova?retryWrites=true&w=majority"

client = pymongo.MongoClient(MONGODB_URI)
inolova = client.inolova
coffee = inolova.coffee
coffee.create_index([("SKU", pymongo.DESCENDING)], unique=True)

COFFEE_MACHINES_PRODUCT_TYPES = ["COFFEE_MACHINE_LARGE", "COFFEE_MACHINE_SMALL", "ESPRESSO_MACHINE"]
WATER_LINE_COMPATIBLES = [True, False]

COFFEE_PODS_PRODUCT_TYPES = ["COFFEE_POD_LARGE", "COFFEE_POD_SMALL", "ESPRESSO_POD"]
COFFEE_PODS_FLAVORS = ["COFFEE_FLAVOR_VANILLA", "COFFEE_FLAVOR_CARAMEL", "COFFEE_FLAVOR_PSL",
                       "COFFEE_FLAVOR_MOCHA", "COFFEE_FLAVOR_HAZELNUT"]
COFFEE_PODS_PACK_SIZES = [1, 3, 5, 7]

# coffee_item = {"SKU":"EP017","product_type":"ESPRESSO_POD","coffee_flavor":"COFFEE_FLAVOR_CARAMEL","pack_size":5}
# print(coffee.insert_one(coffee_item))


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def get_response(coffee_filter):
    result = list(coffee.find(coffee_filter, {'_id': 0}))
    print(coffee_filter)
    coffee_count = len(result)
    if coffee_count == 0:
        err = {"error": "no products match given criteria: {}".format(coffee_filter)}
        return jsonify(err), 404
    response = {"success": True, "count": coffee_count, "payload": result}
    return jsonify(response), 200


@app.route('/api/COFFEE_MACHINES', methods=['GET'])
@cross_origin()
def get_coffee_machines():
    product_type = request.args.get('product_type')
    water_line_compatible = request.args.get('water_line_compatible')

    coffee_filter = {'product_type': {'$regex': ".*MACHINE.*"}}

    if product_type is not None:
        product_type = product_type.upper()
        if product_type not in COFFEE_MACHINES_PRODUCT_TYPES:
            err = {"error": "product_type not found in {}".format(COFFEE_MACHINES_PRODUCT_TYPES)}
            return jsonify(err), 400
        coffee_filter["product_type"] = product_type

    if water_line_compatible is not None:
        water_line_compatible = (water_line_compatible.upper() == "TRUE")
        if water_line_compatible not in WATER_LINE_COMPATIBLES:
            err = {"error": "water_line_compatible not found in {}".format(WATER_LINE_COMPATIBLES)}
            return jsonify(err), 400
        coffee_filter["water_line_compatible"] = water_line_compatible

    return get_response(coffee_filter)


@app.route('/api/COFFEE_PODS', methods=['GET'])
@cross_origin()
def get_coffee_pods():
    product_type = request.args.get('product_type')
    coffee_flavor = request.args.get('coffee_flavor')
    pack_size = request.args.get('pack_size')

    coffee_filter = {'product_type': {'$regex': ".*POD.*"}}

    if product_type is not None:
        product_type = product_type.upper()
        if product_type not in COFFEE_PODS_PRODUCT_TYPES:
            err = {"error": "product_type not found in {}".format(COFFEE_PODS_PRODUCT_TYPES)}
            return jsonify(err), 400
        coffee_filter["product_type"] = product_type

    if coffee_flavor is not None:
        coffee_flavor = coffee_flavor.upper()
        if coffee_flavor not in COFFEE_PODS_FLAVORS:
            err = {"error": "coffee_flavor not found in {}".format(COFFEE_PODS_FLAVORS)}
            return jsonify(err), 400
        coffee_filter["coffee_flavor"] = coffee_flavor

    if pack_size is not None:
        pack_size = int(pack_size)
        if pack_size not in COFFEE_PODS_PACK_SIZES:
            err = {"error": "pack_size not found in {}".format(COFFEE_PODS_PACK_SIZES)}
            return jsonify(err), 400
        coffee_filter["pack_size"] = pack_size

    return get_response(coffee_filter)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

import pymongo
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

MONGODB_URI = "mongodb+srv://ayman:inolova_pass@cluster0-979xj.mongodb.net/inolova?retryWrites=true&w=majority"

# connect to the required mongodb collection, edit this if your database/collection name is different
client = pymongo.MongoClient(MONGODB_URI)
inolova = client.inolova
coffee = inolova.coffee

# making sure SKUs are unique, essential to avoid duplicate products
coffee.create_index([("SKU", pymongo.DESCENDING)], unique=True)

# defining reference strings and values
COFFEE_MACHINES_PRODUCT_TYPES = ["COFFEE_MACHINE_LARGE", "COFFEE_MACHINE_SMALL", "ESPRESSO_MACHINE"]
WATER_LINE_COMPATIBLES = [True, False]

COFFEE_PODS_PRODUCT_TYPES = ["COFFEE_POD_LARGE", "COFFEE_POD_SMALL", "ESPRESSO_POD"]
COFFEE_PODS_FLAVORS = ["COFFEE_FLAVOR_VANILLA", "COFFEE_FLAVOR_CARAMEL", "COFFEE_FLAVOR_PSL",
                       "COFFEE_FLAVOR_MOCHA", "COFFEE_FLAVOR_HAZELNUT"]
COFFEE_PODS_PACK_SIZES = [1, 3, 5, 7]

app = Flask(__name__)
# configure cross-origin request support
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def get_response(coffee_filter):
    """
    applies a mongodb filter to the coffee collection and returns a properly formatted JSON response if the filter
    returns a valid response, or returns an error response if no matching data is found
    :param coffee_filter: mongodb filter to be used on the inolova.coffee collection
    :return: a tuple (response, status_code) if the filter retunrs any result
            OR an error object if no result matches the filter
    """

    # find all matching filter and exclude object id field
    result = list(coffee.find(coffee_filter, {'_id': 0}))
    coffee_count = len(result)
    if coffee_count == 0:
        err = {"error": "no products match given criteria: {}".format(coffee_filter)}
        # if no data is found, return error with appropriate status code
        return jsonify(err), 404
    response = {"success": True, "count": coffee_count, "payload": result}
    return jsonify(response), 200


# for API documentation and examples, check readme.md
@app.route('/api/COFFEE_MACHINES', methods=['GET'])
@cross_origin()
def get_coffee_machines():
    product_type = request.args.get('product_type')
    water_line_compatible = request.args.get('water_line_compatible')

    # initialize filter to only include coffee machines, in case no product_type parameter is included in the request
    coffee_filter = {'product_type': {'$regex': ".*MACHINE.*"}}

    # check url parameters validity and add them to the filter if valid

    if product_type is not None:
        product_type = product_type.upper()
        if product_type not in COFFEE_MACHINES_PRODUCT_TYPES:
            # if parameter value is not expected, return an explanatory error with the proper status code
            err = {"error": "product_type not found in {}".format(COFFEE_MACHINES_PRODUCT_TYPES)}
            return jsonify(err), 400
        # if parameter exists and is valid, add to the filter
        coffee_filter["product_type"] = product_type

    if water_line_compatible is not None:
        water_line_compatible = (water_line_compatible.upper() == "TRUE")
        if water_line_compatible not in WATER_LINE_COMPATIBLES:
            # if parameter value is not expected, return an explanatory error with the proper status code
            err = {"error": "water_line_compatible not found in {}".format(WATER_LINE_COMPATIBLES)}
            return jsonify(err), 400
        # if parameter exists and is valid, add to the filter
        coffee_filter["water_line_compatible"] = water_line_compatible

    # after adding parameters and if no invalid parameter is encountered, apply filter and return result
    return get_response(coffee_filter)


@app.route('/api/COFFEE_PODS', methods=['GET'])
@cross_origin()
def get_coffee_pods():
    product_type = request.args.get('product_type')
    coffee_flavor = request.args.get('coffee_flavor')
    pack_size = request.args.get('pack_size')

    # initialize filter to only include coffee pods, in case no product_type parameter is included in the request
    coffee_filter = {'product_type': {'$regex': ".*POD.*"}}

    # check url parameters validity and add them to the filter if valid

    if product_type is not None:
        product_type = product_type.upper()
        if product_type not in COFFEE_PODS_PRODUCT_TYPES:
            # if parameter value is not expected, return an explanatory error with the proper status code
            err = {"error": "product_type not found in {}".format(COFFEE_PODS_PRODUCT_TYPES)}
            return jsonify(err), 400
        # if parameter exists and is valid, add to the filter
        coffee_filter["product_type"] = product_type

    if coffee_flavor is not None:
        coffee_flavor = coffee_flavor.upper()
        if coffee_flavor not in COFFEE_PODS_FLAVORS:
            # if parameter value is not expected, return an explanatory error with the proper status code
            err = {"error": "coffee_flavor not found in {}".format(COFFEE_PODS_FLAVORS)}
            return jsonify(err), 400
        # if parameter exists and is valid, add to the filter
        coffee_filter["coffee_flavor"] = coffee_flavor

    if pack_size is not None:
        pack_size = int(pack_size)
        if pack_size not in COFFEE_PODS_PACK_SIZES:
            # if parameter value is not expected, return an explanatory error with the proper status code
            err = {"error": "pack_size not found in {}".format(COFFEE_PODS_PACK_SIZES)}
            return jsonify(err), 400
        # if parameter exists and is valid, add to the filter
        coffee_filter["pack_size"] = pack_size

    # after adding parameters and if no invalid parameter is encountered, apply filter and return result
    return get_response(coffee_filter)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

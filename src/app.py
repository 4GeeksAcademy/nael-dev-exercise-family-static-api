"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return jsonify(response_body), 200


@app.route('/members/<int:id>', methods=['GET'])
def handle_oneMember(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Member not found"}), 404


@app.route('/members', methods=['POST'])
def handle_addMember():
    member = request.get_json()
    jackson_family.add_member(member)

    return jsonify({"message": "Miembro agregado correctamente"}), 200
 except ValueError as e:
        return jsonify({"error": str(e)}), 400
except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado"}), 500

@app.route('/members/<int:id>', methods=['DELETE'])
def handle_deleteMember(id):
    deleted = jackson_family.delete_member(id)
    if deleted is True:
        return jsonify({"message": "Miembro eliminado correctamente"}),200
    elif deleted is False:
        return jsonify({"error": "El miembro no se ha podido eliminar"}),400
    elif deleted is None:
        return jsonify({"error": "La id no esta asociada a ningun miembro de la familia"}),404

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

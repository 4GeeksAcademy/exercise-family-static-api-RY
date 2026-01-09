import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure  


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

if len(jackson_family.get_all_members()) == 0:
    jackson_family.add_member({
        "first_name": "John",
        "age": 33,
        "lucky_numbers": [7, 13, 22]
    })
    jackson_family.add_member({
        "first_name": "Jane",
        "age": 35,
        "lucky_numbers": [10, 14, 3]
    })
    jackson_family.add_member({
        "first_name": "Jimmy",
        "age": 5,
        "lucky_numbers": [1]
    })

def bad_request(msg: str):
    return jsonify({"error": msg}), 400

def not_found(msg: str):
    return jsonify({"error": msg}), 404

def validate_member_payload(payload: dict):
    if not isinstance(payload, dict):
        return False, "Invalid JSON body"
    if "first_name" not in payload or not isinstance(payload["first_name"], str) or not payload["first_name"].strip():
        return False, "Field 'first_name' is required and must be a non-empty string"
    if "age" not in payload or not isinstance(payload["age"], int) or payload["age"] <= 0:
        return False, "Field 'age' is required and must be an integer greater than 0"
    if "lucky_numbers" not in payload or not isinstance(payload["lucky_numbers"], list):
        return False, "Field 'lucky_numbers' is required and must be a list"
    if "id" in payload and not isinstance(payload["id"], int):
        return False, "If provided, 'id' must be an integer"
    return True, None


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member is None:
            return not_found(f"Member with id={member_id} not found")
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/members', methods=['POST'])
def add_member():
    try:
        payload = request.get_json()
        is_valid, err = validate_member_payload(payload)
        if not is_valid:
            return bad_request(err)
        created = jackson_family.add_member(payload) 
        return jsonify(created), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        removed = jackson_family.delete_member(member_id)
        if not removed:
            return jsonify({"error": f"Member with id={member_id} not found"}), 404
        return jsonify({"done": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
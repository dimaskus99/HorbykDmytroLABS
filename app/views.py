from flask import jsonify, request
from . import app

users = []
categories = []
records = []


@app.route('/user', methods=['POST'])
def create_user():
    user_id = len(users) + 1
    name = request.json.get('name')
    users.append({"id": user_id, "name": name})
    return jsonify({"message": "User created", "user": {"id": user_id, "name": name}}), 201


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)


@app.route('/category', methods=['POST'])
def create_category():
    category_id = len(categories) + 1
    name = request.json.get('name')
    categories.append({"id": category_id, "name": name})
    return jsonify({"message": "Category created", "category": {"id": category_id, "name": name}}), 201


@app.route('/record', methods=['POST'])
def create_record():
    record_id = len(records) + 1
    user_id = request.json.get('user_id')
    category_id = request.json.get('category_id')
    amount = request.json.get('amount')
    record = {"id": record_id, "user_id": user_id, "category_id": category_id, "amount": amount}
    records.append(record)
    return jsonify({"message": "Record created", "record": record}), 201


@app.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')

    filtered_records = records
    if user_id:
        filtered_records = [r for r in filtered_records if r['user_id'] == int(user_id)]
    if category_id:
        filtered_records = [r for r in filtered_records if r['category_id'] == int(category_id)]

    return jsonify(filtered_records)

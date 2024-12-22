from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User, Category, Record, Currency
from app.schemas import UserSchema, CategorySchema, RecordSchema, CurrencySchema
from .utils import handle_error
from passlib.hash import pbkdf2_sha256

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        if User.query.filter_by(name=data['name']).first():
            return jsonify({"message": "User with this name already exists"}), 400

        hashed_password = pbkdf2_sha256.hash(data['password'])
        new_user = User(name=data['name'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return handle_error(e)

@api_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json

        user = User.query.filter_by(name=data['name']).first()
        if not user or not pbkdf2_sha256.verify(data['password'], user.password):
            return jsonify({"message": "Invalid username or password"}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    except Exception as e:
        return handle_error(e)
@api_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
@api_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = User.query.all()
        return jsonify(UserSchema(many=True).dump(users))
    except Exception as e:
        return handle_error(e)

@api_bp.route('/category', methods=['POST'])
@jwt_required()
def create_category():
    try:
        data = request.json
        errors = CategorySchema().validate(data)
        if errors:
            return jsonify(errors), 400

        category = Category(name=data['name'])
        db.session.add(category)
        db.session.commit()

        return jsonify({"message": "Category created", "category": CategorySchema().dump(category)}), 201
    except Exception as e:
        return handle_error(e)

@api_bp.route('/record', methods=['POST'])
@jwt_required()
def create_record():
    try:
        data = request.json
        errors = RecordSchema().validate(data)
        if errors:
            return jsonify(errors), 400

        record = Record(user_id=data['user_id'], category_id=data['category_id'], amount=data['amount'])
        db.session.add(record)
        db.session.commit()

        return jsonify({"message": "Record created", "record": RecordSchema().dump(record)}), 201
    except Exception as e:
        return handle_error(e)

@api_bp.route('/records', methods=['GET'])
@jwt_required()
def get_records():
    try:
        user_id = request.args.get('user_id', type=int)
        category_id = request.args.get('category_id', type=int)

        query = Record.query
        if user_id:
            query = query.filter_by(user_id=user_id)
        if category_id:
            query = query.filter_by(category_id=category_id)

        records = query.all()
        return jsonify(RecordSchema(many=True).dump(records))
    except Exception as e:
        return handle_error(e)

@api_bp.route('/currency', methods=['POST'])
@jwt_required()
def create_currency():
    try:
        data = request.json
        errors = CurrencySchema().validate(data)
        if errors:
            return jsonify(errors), 400

        currency = Currency(name=data['name'], code=data['code'])
        db.session.add(currency)
        db.session.commit()

        return jsonify({"message": "Currency created", "currency": CurrencySchema().dump(currency)}), 201
    except Exception as e:
        return handle_error(e)

@api_bp.route('/currencies', methods=['GET'])
@jwt_required()
def get_currencies():
    try:
        currencies = Currency.query.all()
        return jsonify(CurrencySchema(many=True).dump(currencies))
    except Exception as e:
        return handle_error(e)

@api_bp.route('/user/<int:user_id>/default_currency', methods=['PUT'])
@jwt_required()
def set_default_currency(user_id):
    try:
        data = request.json
        currency_id = data.get('currency_id')

        user = User.query.get_or_404(user_id)
        currency = Currency.query.get_or_404(currency_id)

        user.default_currency_id = currency.id
        db.session.commit()

        return jsonify({"message": f"Default currency for user {user.name} set to {currency.name}."})
    except Exception as e:
        return handle_error(e)

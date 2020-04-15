import os
from app import app, db
from flask import jsonify
from flask import render_template, request, redirect, url_for, flash, make_response, session
from .models import User,UserSchema,CreateInputSchema,CreateLoginSchema
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity)


user_schema = UserSchema()
create_input_schema = CreateInputSchema()
create_login_schema = CreateLoginSchema()


@app.route("/user/<user_id>", methods =['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
       return jsonify({"message": "user does not exist"}), 404
    print(user.name)
    result = user_schema.dump(user)
    return jsonify({"data": result,"status": "202"}), 202


@app.route("/user/all", methods =['GET'])
def get_user_all():
    all_records = User.query.all()
    list = []
    for record in all_records:
        list.append(record.username)
    return jsonify({"Msg":"all usernames","data":list})



@app.route("/user/<user_id>", methods =['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()    
    if user is None:
        return jsonify({"message": "user does not exist"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "user deleted"}), 202


@app.route("/user", methods =['POST'])
def post_user():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
# for request it is necessary: name, username, email, number_telephone, password
    errors = create_input_schema.validate(request.json)
    print(errors)
    if errors:
        return jsonify({"msg":"BAD REQUEST"})
    data = request.get_json()
    existing_user = User.query.filter_by(name=data['name']).first()
    if existing_user is not None:
        return jsonify({"message": "user already exists","error":403}), 403
    new_user = User(name=data['name'], username=data['username'],email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg":"user is registered"})


# плохо - меняется created_on
@app.route("/user", methods =['PUT'])
def put_user():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
# for request it is necessary: name, username, email, number_telephone, password
    errors = create_input_schema.validate(request.json)
    if errors:
        return jsonify({"msg": "BAD REQUEST"})
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user:
        user_check = user.check_password(data["password"])
        if user_check:
# data["number_telephone"] add if necessary
            user_change = User(name=data["name"],username=data['username'],email=data["email"])
            user_change.set_password(data['password'])
            db.session.delete(user)
            db.session.commit()
            db.session.add(user_change)
            db.session.commit()
            return jsonify({"msg": "user data changed"})
    return jsonify({"msg": "Bad username or password", "error": 401}), 401


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
# for request it is necessary: username, password
    errors = create_login_schema.validate(request.json)
    if errors:
        return jsonify({"msg":"BAD REQUEST"})
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username = username).first()
    if user:
        user_check = user.check_password(password)
        if user_check:
            obj = {"identity": username, "test": 12345}
            access_token = create_access_token(identity=obj)
            return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password","error":401}), 401


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

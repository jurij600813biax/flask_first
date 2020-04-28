import os
from app import app, db
from flask import jsonify
from flask import render_template, request, redirect, url_for, flash, make_response, session
from .models import User, Product, UserSchema, CreateInputSchema, CreateLoginSchema, CreateProductSchema
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity)
from werkzeug.utils import secure_filename

user_schema = UserSchema()
create_input_schema = CreateInputSchema()
create_login_schema = CreateLoginSchema()
create_product_schema = CreateProductSchema()


@app.route("/")
def index():
    return render_template('index.html', name="Jurij")


@app.route("/user/<user_id>", methods =['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if request.is_json:
        if user is None:
            return jsonify({"message": "user does not exist"}), 404
        print(user.name)
        result = user_schema.dump(user)
        return jsonify({"data": result, "status": "202"}), 202
    return "Profile page of user #{},name - {},username - {}".format(user_id, user.name, user.username)


@app.route("/user/all", methods =['GET'])
def get_user_all():
    all_records = User.query.all()
    list = []
    for record in all_records:
        list.append(record.username)
    if request.is_json:
        return jsonify({"Msg": "all usernames", "data": list})
    return "All users {}".format(list)


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
    new_user = User(name=data['name'], username=data['username'],email=data['email'],
                    number_telephone=data['number_telephone'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg":"user is registered"})


@app.route("/user", methods =['PUT'])
def put_user():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
# for request it is necessary: name, username, email, number_telephone, password
# can be changed: name, email, number_telephone
    errors = create_input_schema.validate(request.json)
    if errors:
        return jsonify({"msg": "BAD REQUEST"})
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user:
        user_check = user.check_password(data["password"])
        if user_check:
            user.number_telephone = data['number_telephone']
            user.name = data["name"]
            user.email = data["email"]
            db.session.add(user)
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

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/product_input_photo',methods=['POST'])
def post_product_photo():
    if not request.is_json:
    # Filename: Photo-productid-1234453465654.jpg (Unix Timestamp)
    # Content-Type (image/jpeg)
    # Extension (.jpg)
    #    request.files['file2'].save("/home/jurij/flask_first/uploads/first-file-upload.jpg")
#        file = request.files['file1']
#                return "Total uploaded files: " + str(len(request.files)
        for file in request.files.getlist('test'):
            if allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        return jsonify("Photo OK")
    return jsonify("Format must not be json")

@app.route('/product_input_multi', methods=['POST'])
def post_product_multi():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    errors = create_product_schema.validate(request.json)
    print(errors)
    if errors:
        return jsonify({"msg": "BAD REQUEST"})
    data = request.get_json()
    existing_product = Product.query.filter_by(product_code=data['product_code']).first()
    if existing_product is not None:
        return jsonify({"message": "product already exists", "error": 403}), 403
    new_product = Product(
        product_code=data['product_code'],
        product_quantity=data['product_quantity'],
        product_quality=data['product_quality'],
        product_comment=data['product_comment'],
        product_color=data['product_color'],
        product_size=data['product_size'],
        product_supplier=data['product_supplier'],
        product_photo=data['product_photo'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify("OK")


@app.route('/product_input_multi', methods=['PUT'])
def put_product_multi():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    errors = create_product_schema.validate(request.json)
    print(errors)
    if errors:
        return jsonify({"msg": "BAD REQUEST"})
    data = request.get_json()
    product = Product.query.filter_by(product_code=data['product_code']).first()
    if product is None:
        return jsonify({"message": "product does not exist"})
    product.product_quantity = data['product_quantity']
    product.product_quality = data['product_quality']
    product.product_comment = data['product_comment']
    product.product_color = data['product_color']
    product.product_size = data['product_size']
    product.product_supplier = data['product_supplier']
    product.product_photo = data['product_photo']
    db.session.add(product)
    db.session.commit()
    return jsonify({"msg": "product data changed"})

from flask_restful import Resource, Api
from flask import render_template, request, redirect, url_for, flash, make_response, session
from flask import jsonify


class Product(Resource):
    def post(self):

        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
#        data = request.get_json()
        return jsonify({"msg": "file OK"})

    def get(self):
        return jsonify({"msg": "GET OK"})
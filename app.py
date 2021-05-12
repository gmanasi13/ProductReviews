"""

ISI Coding test: Product Reviews backend
This is the main file that runs and launches the flask app

For simplicity, for items not in DB, return a status code of 200
as the request has been executed successfully

status code 400 is returned when its an invalid input sent in
the request

Author: Manasi Godse
Date: May 7th, 2021

"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


class Serializer(object):
    """ This class serializes the output of the GET request so that it can work with jsonify"""

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


# Setup the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:secret@db:5432/isi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = False
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

# models are imported here since models.py had a dependency on the Serializer class defined above
from models import Products, Reviews, Users


# GEt method /user/{user_id}
@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'Status Code': 200, 'message': 'No such user exists'}), 200
    return jsonify(user.serialize()), 200


# GET method /product/{product_id}
@app.route('/product/<product_id>', methods=['GET'])
def get_product(product_id):
    product = Products.query.get(product_id)
    if product is None:
        return jsonify({'Status Code': 200, 'message': 'No such product exists'}), 200
    return jsonify(product.serialize()), 200


# GET method /review/{product_id}
@app.route('/review/<product_id>', methods=['GET'])
def get_reviews(product_id):
    if request.method == 'GET':
        product = Products.query.get(product_id)
        if product is None:
            return jsonify({'Status Code': 200, 'message': 'No such product exists'}), 200

        reviews = Reviews.query.filter(Reviews.product_id == product_id)
        if reviews.count() == 0:
            return jsonify({'Status Code': 200, 'message': 'No Review exists'}), 200
        return jsonify(Reviews.serialize_list(reviews)), 200


# POST and PUT method /review/{product_id}
@app.route('/review/<product_id>', methods=['PUT', 'POST'])
def insert_reviews(product_id):
    user_id = request.form.get('user_id')
    review = request.form.get('review')
    rating = request.form.get('rating')

    product = Products.query.get(product_id)
    if product is None:
        return jsonify({'Status Code': 200, 'message': 'No such product exists'}), 200

    if validate_input(user_id, review, rating):
        reviewExists = Reviews.query.filter(Reviews.user_id == user_id, Reviews.product_id == product_id).first()
        if reviewExists is not None and request.method == 'POST':
            return jsonify(
                {'Status Code': 400, 'message': 'Multiple reviews by same user for one product not permitted'}), 400

        else:
            new_review = Reviews(product_id=product_id, user_id=user_id, review=review, rating=rating)
            user_id = int(user_id)
            rating = float(rating)
            if request.method == 'POST':
                db.session.add(new_review)
            else:
                reviewExists.product_id = product_id
                reviewExists.user_id = int(user_id)
                reviewExists.review = review
                reviewExists.rating = int(rating)
        db.session.commit()
        response = jsonify({'product_id': new_review.product_id,
                            'user_id': new_review.user_id,
                            'review': new_review.review,
                            'rating': new_review.rating})
        response.status_code = 200
        return response

    else:
        return jsonify({'Status Code': 400, 'message': 'Invalid Input'}), 400


# DELETE method /review/{product_id}
@app.route('/review/<product_id>', methods=['DELETE'])
def delete_review(product_id):
    user_id = request.form.get('user_id')
    if user_id is None or not user_id.isdigit():
        return jsonify({'Status Code': 400, 'message': 'Invalid Input'}), 400
    review = Reviews.query.filter(Reviews.user_id == user_id, Reviews.product_id == product_id).first()
    if review is None:
        return jsonify({'Status Code': 200, 'message': 'No review found to delete'}), 200
    db.session.delete(review)
    db.session.commit()
    return jsonify({'Success': 'Review deleted successfully'}), 200


# Validate the input at the application level as raising exceptions using SQL is expensive
def validate_input(user_id, review, rating):
    if user_id is None or not user_id.isdigit():
        return False
    if review is None:
        return False
    if rating is None:
        return False
    else:
        try:
            value = float(rating)
            if value >= 1.0 or value <= 5.0:
                return True
        except ValueError:
            return False

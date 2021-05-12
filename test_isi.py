"""
ISI Coding test: Product Reviews backend
Unit tests to test the REST APIs
Author: Manasi Godse
Date: May 7th, 2021

Following tests (includes negative testing) are executed:

1. GET user_id
2. GET product_id
3. GET review for a product_id
4. POST review for product_id
5. PUT review for product_id
6. DELETE review for product_id
"""


import unittest
import os
import json
from app import db, app
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


def print_line():
    print("================")


class ISITestCase(unittest.TestCase):
    """Configurations for Testing, with a separate test database."""

    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:secret@db:5432/'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = False
        db = SQLAlchemy(app)
        db.Model.metadata.reflect(db.engine)
        db.create_all()

    def test_api_get_users(self):
        print("\nTesting API: GET --> /user/3\n")
        resp = self.app.get('/user/3')
        print(json.loads(resp.data))
        print_line()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(3, resp.json['id'])

    def test_user_not_exists(self):
        print("\nNegative Testing API: GET --> /user/6\n")
        resp = self.app.get('/user/6')
        print(json.loads(resp.data))
        print_line()
        self.assertEqual(resp.status_code, 200)

    def test_api_get_reviews(self):
        print("\nTesting API: GET --> /review/4\n")
        resp = self.app.get('/review/4')
        print(json.loads(resp.data))
        print_line()
        self.assertEqual(resp.status_code, 200)

    def test_review_not_exists(self):
        print("\n Testing API: GET --> /review/2\n")
        resp = self.app.get('/review/2')
        print(json.loads(resp.data))
        print_line()
        self.assertEqual(resp.status_code, 200)

    def test_review_no_product(self):
        print("\n Negative Testing API: GET --> /review/12\n")
        resp = self.app.get('/review/12')
        print(json.loads(resp.data))
        print_line()
        self.assertEqual(resp.status_code, 200)

    def test_api_get_product(self):
        print("\nTesting API: GET --> /product/7\n")
        resp = self.app.get('/product/7')
        print(json.loads(resp.data))
        print_line()
        self.assertEqual(resp.status_code, 200)

    def test_api_product_not_exists(self):
        print("\n Negative Testing API: GET --> /product/11\n")
        resp = self.app.get('/product/11')
        print(json.loads(resp.data))
        print_line()
        self.assertEqual(resp.status_code, 200)

    def test_api_post_review(self):
        user_id = 5
        payload = {"user_id": user_id}
        resp = self.app.delete('/review/7', data=payload)

        print("\n Testing API: POST --> /review/7\n")
        user_id = 5
        review = "Did not find it that useful. Weak in durability"
        rating = 2.5
        payload = {"user_id": user_id, "review": review, "rating": rating}
        resp = self.app.post('/review/7', data=payload)
        print(json.loads(resp.data))
        print_line()
        self.assertEqual(resp.status_code, 200)

    def test_api_post_review_invalid_input(self):
        print("\n Testing API with Invalid Input POST --> /review/4\n")
        user_id = "test"
        review = "Did not find it that useful. Weak in durability"
        rating = 2.5
        payload = {"user_id": user_id, "review": review, "rating": rating}
        resp = self.app.post('/review/7', data=payload)
        print(json.loads(resp.data))
        print_line()
        self.assertEqual(resp.status_code, 400)

    def test_api_post_multiplereviews(self):
        user_id = 5
        review = "Did not find it that useful. Weak in durability"
        rating = 2.5
        payload = {"user_id": user_id, "review": review, "rating": rating}
        resp = self.app.post('/review/8', data=payload)

        print("\n Testing Multiple product review from same user API: POST --> /review/7\n")
        user_id = 5
        review = "Did not find it that useful. Weak in durability"
        rating = 2.5
        payload = {"user_id": user_id, "review": review, "rating": rating}

        resp = self.app.post('/review/8', data=payload)
        print(json.loads(resp.data))
        print_line()
        self.assertEqual(resp.status_code, 400)

    def test_api_put_review(self):
        user_id = 5
        review = "works great"
        rating = 4.5
        payload = {"user_id": user_id, "review": review, "rating": rating}
        resp = self.app.post('/review/6', data=payload)

        print("\n Testing API: PUT --> /review/6\n")
        user_id = 5
        review = "Edit: broke after few days"
        rating = 2.5
        payload = {"user_id": user_id, "review": review, "rating": rating}
        resp = self.app.put('/review/6', data=payload)
        print(resp.data)
        print_line()
        self.assertEqual(resp.status_code, 200)

        user_id = 5
        payload = {"user_id": user_id}
        resp = self.app.delete('/review/7', data=payload)

    def test_api_delete_review(self):
        print("\n Testing API: DELETE --> /review/7\n")
        user_id = 5
        payload = {"user_id": user_id}
        resp = self.app.delete('/review/7', data=payload)
        print(resp.data)
        print_line()
        self.assertEqual(resp.status_code, 200)

    def test_api_delete_no_review(self):
        print("\n Testing API: DELETE --> /review/9\n")
        user_id = 5
        payload = {"user_id": user_id}
        resp = self.app.delete('/review/7', data=payload)
        print(resp.data)
        print_line()
        self.assertEqual(resp.status_code, 200)

    def test_api_delete_review_invalid_input(self):
        print("\n Testing API with Invalid Input DELETE --> /review/4\n")
        user_id = "test"
        payload = {"user_id": user_id}
        resp = self.app.post('/review/4', data=payload)
        print(json.loads(resp.data))
        print_line()
        self.assertEqual(resp.status_code, 400)

    def tearDown(self):
        db.session.remove()
        # Not dropping the db now since it is not create automatically using ORM
        # db.drop_all()


if __name__ == "__main__":
    unittest.main()

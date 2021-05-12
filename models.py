"""
ISI Coding test: Product Reviews backend
Models.py defines the tables as models using SQLAlchemy
Tables are already create in Postgres manually

Author: Manasi Godse
Date: May 7th, 2021
"""

from app import db, Serializer
db.Model.metadata.reflect(db.engine)

class Products(db.Model, Serializer):
    """ Represents the products table """
    __tablename__ = 'products'
    id = db.Column('id',db.Integer, primary_key=True)
    #__table__ = db.Model.metadata.tables['products']


class Users(db.Model, Serializer):
    """ Represents the user table"""
    __tablename__ = 'users'
    #__table__ = db.Model.metadata.tables['users']
    id = db.Column('id',db.Integer, primary_key=True)
	#__table__ = db.Model.metadata.tables['users']


class Reviews(db.Model, Serializer):
    """ Represents the Reviews table"""
    __tablename__ = 'reviews'
    id = db.Column('id',db.Integer, primary_key=True)

#__table__ = db.Model.metadata.tables['reviews']

    """ Construction defined as Insertion happens via ORM """

    def __init__(self, user_id, product_id, review, rating):
        self.user_id = user_id
        self.product_id = product_id
        self.review = review
        self.rating = rating


def save(self):
    db.session.add(self)
    db.session.commit()


def delete(self):
    db.session.delete(self)
    db.session.commit()

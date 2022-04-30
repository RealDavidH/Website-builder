from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt, cloudinary
from flask import flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import re
from flask_app.models.model_user import User
from cloudinary import uploader
# from flask_app.models.model_like import Like
#!!!!!!!!!!!!!!!!!!!!!!!!CHANGE MODEL FILE NAME!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class Carousel:
    def __init__(self, data):
        self.id = data['id']
        self.url = data['url']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM carousels;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances
        if results:
            carousels = []
            # ^ assign var name and return that var
        # Iterate over the db results and create instances of friends with cls.
            for carousel in results:
                # ^ assign var name
                carousels.append(cls(carousel))
                # ^ assign var name
            return carousels  # return that var you named on the list
        return False

    @classmethod
    def get_one(cls, data: dict) -> object:
        print(data)
        query = "SELECT * FROM carousels where id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])

    @classmethod
    def create(cls, data: dict) -> object:
        print(data)
        query = "insert into carousels (url, public_id) values (%(url)s, %(public_id)s)"
        carousel_id = connectToMySQL(DATABASE).query_db(query, data)
        return carousel_id  # ^ assign var name and return that var

    @classmethod
    def delete(cls, data: dict) -> object:
        print(data)
        carousel.destoy_public_id(data)
        query = "delete from carousels where post_id = %(post_id)s"
        connectToMySQL(DATABASE).query_db(query, data)
        print('Delete carousel')

    @staticmethod
    def destoy_carousel_public_id(data):
        print(data)
        query = "SELECT public_id FROM carousels where id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        cloudinary.uploader.destroy(results['public_id'])
        print('deleting public ids')

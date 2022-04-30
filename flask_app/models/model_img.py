from flask_app.config.mysqlconnection import connectToMySQL
# change this to your database name in __init__ file
from flask_app import DATABASE, bcrypt, cloudinary
from flask import flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import re
from flask_app.models.model_user import User
from cloudinary import uploader
# from flask_app.models.model_like import Like
#!!!!!!!!!!!!!!!!!!!!!!!!CHANGE MODEL FILE NAME!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class Image:
    def __init__(self, data):
        self.id = data['id']
        self.url = data['url']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.post_id = data['post_id']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM images;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances
        if results:
            images = []
            # ^ assign var name and return that var
        # Iterate over the db results and create instances of friends with cls.
            for image in results:
                # ^ assign var name
                images.append(cls(image))
                # ^ assign var name
            return images  # return that var you named on the list
        return False

    @classmethod
    def get_one(cls, data: dict) -> object:
        print(data)
        query = "SELECT * FROM images where id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])

    @classmethod
    def get_one_post_id(cls, data: dict) -> object:
        print(data)
        query = "SELECT * FROM images where post_id = %(post_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
    # @classmethod
    # def join_images_one(cls, data:dict) -> object:
    #     query = "select *, users.first_name from images left join users on users.id = images.user_id where images.id = %(id)s"
    #     image_joined = connectToMySQL(DATABASE).query_db(query, data)
    #     return image_joined

    @classmethod
    def create(cls, data: dict) -> object:
        print(data)
        query = "insert into images (url, public_id, post_id) values (%(url)s, %(public_id)s, %(post_id)s)"
        image_id = connectToMySQL(DATABASE).query_db(query, data)
        return image_id  # ^ assign var name and return that var

    @classmethod
    def delete(cls, data: dict) -> object:
        print(data)
        Image.destoy_public_id(data)
        query = "delete from images where post_id = %(post_id)s"
        connectToMySQL(DATABASE).query_db(query, data)
        print('Delete image')

    @staticmethod
    def destoy_public_id(data):
        print(data)
        query = "SELECT public_id FROM images where post_id = %(post_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            for public_id in results:
                cloudinary.uploader.destroy(public_id['public_id'])
        print('deleting public ids')

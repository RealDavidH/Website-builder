import mimetypes
from flask_app.config.mysqlconnection import connectToMySQL
# change this to your database name in __init__ file
from flask_app import DATABASE, bcrypt, cloudinary
from flask import flash, request, redirect, session
from flask_app.models.model_img import Image

import re
from flask_app.models.model_user import User
# from flask_app.models.model_like import Like
#!!!!!!!!!!!!!!!!!!!!!!!!CHANGE MODEL FILE NAME!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class News:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        # self.created_at = data['created_at']
        # self.updated_at = data['updated_at']
        # self.user_id = data['user_id']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances
        if results:
            news = []
            # ^ assign var name and return that var
        # Iterate over the db results and create instances of friends with cls.
            for new in results:
                # ^ assign var name
                news.append(cls(new))
                # ^ assign var name
            return news  # return that var you named on the list
        return False

    @classmethod
    def get_one(cls, data: dict) -> object:
        print(data)
        query = "SELECT * FROM posts where id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if results:
            return cls(results[0])

    # @classmethod
    # def join_news(cls):
    #     query = "select *, users.first_name from news left join users on users.id = news.user_id;"
    #     new_joined = connectToMySQL(DATABASE).query_db(query)
    #     return new_joined
    
    # @classmethod
    # def join_news_one(cls, data:dict) -> object:
    #     query = "select *, users.first_name from news left join users on users.id = news.user_id where news.id = %(id)s"
    #     new_joined = connectToMySQL(DATABASE).query_db(query, data)
    #     return new_joined

    @classmethod
    def create(cls, data: dict) -> object:
        print(data)
        query = "insert into posts (title, content) values (%(title)s, %(content)s)"
        new_id = connectToMySQL(DATABASE).query_db(query, data)
        return new_id  # ^ assign var name and return that var

    @classmethod
    def update_one(cls, data: dict) -> object:
        print(data)
        query = "UPDATE posts SET title = %(title)s, content = %(content)s where id = %(id)s"
        connectToMySQL(DATABASE).query_db(query, data)
        print('Update')

    @classmethod
    def delete_one(cls, data: dict) -> object:
        print(data)
        query = "delete from posts where id = %(id)s"
        connectToMySQL(DATABASE).query_db(query, data)
        print('Delete new')

    @staticmethod
    def validate(form_data: dict):
        print(form_data)
        fields = "One, or more of the required fields are blank."
        if len(form_data['title']) <= 0:
            flash(fields, "err_blank")
            return False
        if len(form_data['content']) <= 0:
            flash(fields, "err_blank")
            return False
        return True

    @property
    def get_img_url(self) -> object:
        print(self.id)
        img = Image.get_one_post_id({'post_id': self.id})
        img_url = img.url
        print(img_url, "Image url")
        return img_url


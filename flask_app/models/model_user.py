from types import NoneType
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt #change this to your database name in __init__ file
from flask import flash, session
import re	

#!!!!!!!!!!!!!!!!!!!!!!!!CHANGE MODEL FILE NAME!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM admins;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances 
        if results:
            admins = []
            #^ assign var name and return that var
        # Iterate over the db results and create instances of friends with cls.
            for admin in results:
            #^ assign var name 
                admins.append( cls(admin) )
                #^ assign var name 
            return admins #return that var you named on the list


    @classmethod
    def get_one(cls, data:dict) -> object:
        print(data)
        query = "SELECT * FROM admins where id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False


    @classmethod
    def get_one_email(cls, data):
        print(data, "DATA")
        query = "SELECT * FROM admins where email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            admin = cls(results[0])
            return admin
        return False


    @classmethod
    def create(cls, data:dict) -> object:
        print(data)
        query = "insert into admins (email, password) values (%(email)s, %(password)s)"
        admin_id = connectToMySQL(DATABASE).query_db(query, data)
        return admin_id#^ assign var name and return that var

    @classmethod 
    def delete_one (cls, data:dict) -> object:
        print(data)
        query = "delete from admins where id = %(id)s"
        connectToMySQL(DATABASE).query_db(query, data)
        print('Delete admin')


    @staticmethod
    def check_email(unchek_email):
        emails = User.get_all()
        print(emails)
        if isinstance(emails, NoneType):
            return True
        for email in emails:
            if unchek_email == email.email:
                return False
        return True


    @staticmethod
    def validate(form_data:dict):
        print(form_data)
        fields = "One, or more of the required fields are blank."

        if len(form_data['email']) <= 0:
            flash(fields, "err_blank")
            return False

        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!", "err_email")
            return False

        if not User.check_email(form_data['email']):
            flash("Email already in use!", "err_email")
            return False

        if len(form_data['password']) < 8:
            flash('Password must be longer than 8 characters', 'err_paswrd')
            return False

        if  not True in [char.isalpha() for char in form_data['password']]:
            flash('Password must contain at least 1 letter and 1 number.', 'err_paswrd')
            print("no letter")
            return False

        if not True in [char.isdigit() for char in form_data['password']]:
            print("no number")
            flash('Password must contain at least 1 letter and 1 number.', 'err_paswrd')
            return False

        if form_data['password'] != form_data['chkr_password']:
            flash('Passwords must match!', 'err_paswrd')
            return False
        
        return True


    @staticmethod
    def validate_login(form_data):
        print(form_data)
        fields = "One, or more of the required fields are blank."

        if len(form_data['email']) <= 0:
            flash(fields, "err_blank_log")
            return False

        if  len(form_data['password']) <= 0:
            flash(fields, "err_blank_log")
            return False

        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email and/or password!", "err_invaild_log")
            return False

        if len(form_data['password']) < 8:
            flash('Invalid email and/or password!', 'err_invaild_log')
            return False
        else:
            poten_admin = User.get_one_email({"email": form_data['email']})
            print(poten_admin)
            if not bcrypt.check_password_hash(poten_admin.password, form_data['password']):
                flash('Invalid email and/or password!', 'err_invaild_log')
                return False
            else:
                session['uuid'] = poten_admin.id
        return True



    # def has_liked(self, show_id) -> str:
    #     return Like.has_like({'admin_id': self.id, 'show_id': show_id})
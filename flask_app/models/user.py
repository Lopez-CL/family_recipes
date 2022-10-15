import email
from flask_app import app
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
from flask_app.models import recipe # import other model don't forget
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #my regex
#my bcrypt imports
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
db_name = 'recipe_schema'

# item.py
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = [] #will hold all of a user's recipes

# #My class methods


    @classmethod
    def save(cls,data):
        query = """INSERT INTO users
        (first_name, last_name, email, password)
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
        """
        return connectToMySQL('recipe_schema').query_db(query,data)

    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db_name).query_db(query,data)
        if len(results) == 0:
            return None
        else:
            print('found and grabbing email...')
            return cls(results[0])
    @classmethod 
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db_name).query_db(query,data)
        if len(results) == 0:
            return None
        else:
            print('found and grabbing user id...')
            return cls(results[0])

# my static methods
    @staticmethod
    def validate_reg(reg_data):
        is_valid = True
        if len(reg_data['first_name']) < 2:
            flash("First name must be 2 characters or more!", 'register')
            is_valid = False
        if len(reg_data['last_name']) < 2:
            flash("Last name must be 2 characters or more!", 'register')
            is_valid = False
        #email regex
        if not EMAIL_REGEX.match(reg_data['email']):
            flash("Did not receive a valid email address! Please again.", 'register')
            is_valid = False
        #check if email exists
        email_data = {
            'email': reg_data['email']
        }
        found_user_or_none = User.get_user_by_email(email_data)
        if found_user_or_none != None:
            flash("Email already taken", "register")
            is_valid = False
        if len(reg_data['password']) < 8:
            flash("Password name must be 2 characters or more!", 'register')
            is_valid = False
        if reg_data['password'] != reg_data['confirm_password']:
            flash("Passwords do not match!", 'register')
            is_valid = False
        return is_valid
    @staticmethod
    def validate_login(login_data):
        #remember they need to enter a valid email address
        if not EMAIL_REGEX.match(login_data['email']):
            flash('Invalid login credentials!', 'login')
            return False
        #check to see if user email is in database. Remember to check we need to grab email_data so you will need classmethod
        email_data = {
            'email': login_data['email']
        }
        found_user_or_none = User.get_user_by_email(email_data)
        if found_user_or_none == None:
            flash('Invalid login credentials!', 'login')
            return False
        #lastly check pw
        if not bcrypt.check_password_hash(found_user_or_none.password, login_data['password']):
            flash('Invalid login credentials!', 'login')
            return False
        return found_user_or_none
        
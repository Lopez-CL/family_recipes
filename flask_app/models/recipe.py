from unittest import result
from flask_app import app
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
from flask_app.models import user
#my bcrypt imports
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
db_name = 'recipe_schema'
# item.py
class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.made = data['made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None #this attribute is what you will use for the many category. Remeber there's no empty list here because only one user can be associated with a user.

# #My class methods
    @classmethod
    def save(cls,data):
        query = """INSERT INTO recipes
        (name,description,instructions,made,under_30,user_id)
        VALUES (%(name)s,%(description)s,%(instructions)s,%(made)s,%(under_30)s,%(user_id)s);
        """
        return connectToMySQL(db_name).query_db(query,data)
    #this is what Ive been used used to seeing. Displaying the many while indicating what "one" is to be associated with it.
    @classmethod
    def show_recipes(cls):
        query = """SELECT * FROM recipes
        LEFT JOIN users
        ON recipes.user_id = users.id;
        """
        results = connectToMySQL(db_name).query_db(query)
        print(results)
        all_recipe_objects = [] # to hold all of the many (with the associated user for each many object)
        #results here are a list of dictionaries
        if len(results) == 0:
            return []
        else: 
            for this_recipe_dictionary in results: #allows me to get each dictionary
                this_recipe_object = cls(this_recipe_dictionary) #make a class instance/object of each dictionary
                this_user_dictionary = { #create a distinct user dictionary based on the key-pair-values in the recipe dictionary.
                            'id':this_recipe_dictionary['users.id'], #REMEBER WHERE THERE ARE SIMILAR NAMES FOR VALUES/KEYS MYSQL WILL DISTINGUISH WHERE ONE IS THE SAME NAME OF ANOTHER TABLE. YOU MUST REFLECT THIS IN YOUR CODE
                            'first_name':this_recipe_dictionary['first_name'],
                            'last_name':this_recipe_dictionary['last_name'],
                            'email':this_recipe_dictionary['email'],
                            'password':this_recipe_dictionary['password'],
                            'created_at':this_recipe_dictionary['users.created_at'],
                            'updated_at':this_recipe_dictionary['users.updated_at']
                }
                #crate a class instance/object of user
                this_user_object = user.User(this_user_dictionary)
                #add the class instance/object to your the respective attribute of the other class instance @ line 21
                this_recipe_object.user = this_user_object
                #since we are showing all instances of the many, add each instance/object to the empty list
                all_recipe_objects.append(this_recipe_object)
                #finally return that list
            return all_recipe_objects        
    @classmethod
    def get_recipe_with_user(cls,data): #this was a more specific grab, i.e., one "many" object and it associated user. Therefore, I had to provide the WHERE condition
        query ="""SELECT * FROM recipes
        LEFT JOIN users 
        ON recipes.user_id = users.id
        WHERE recipes.id = %(id)s; 
        """
        # no need for an empty list here because I'm only grabbing one many
        results = connectToMySQL(db_name).query_db(query,data)
        print(results)
        for this_recipe_dictionary in results:
            this_recipe_object = cls(this_recipe_dictionary)
            this_user_dictionary = {
                    'id':this_recipe_dictionary['users.id'],
                    'first_name':this_recipe_dictionary['first_name'],
                    'last_name':this_recipe_dictionary['last_name'],
                    'email':this_recipe_dictionary['email'],
                    'password':this_recipe_dictionary['password'],
                    'created_at':this_recipe_dictionary['users.created_at'],
                    'updated_at':this_recipe_dictionary['users.updated_at']
            }
            this_user_object = user.User(this_user_dictionary)
            this_recipe_object.user = this_user_object
        return this_recipe_object

    @classmethod
    def get_recipe_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        print('grabbing recipe...')
        results = connectToMySQL(db_name).query_db(query,data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])

    @classmethod
    def edit_recipe_db(cls,data):
        query = """UPDATE recipes SET
        name = %(name)s,
        description = %(description)s,
        instructions = %(instructions)s,
        made = %(made)s,
        under_30 = %(under_30)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(db_name).query_db(query,data)
    @classmethod
    def delete_recipe_db(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(db_name).query_db(query,data)

#My Static Methods

    @staticmethod
    def validate_recipe(recipe_data):
        is_valid = True
        #validate first name. #my friend's name is Ty, so our typical validation check excludes if from the app lol
        if len(recipe_data['name']) < 3:
            flash('Name must be 4 characters or more.', 'recipe')
            is_valid = False
        if len(recipe_data['description']) < 3:
            flash('Description must be 4 characters or more.', 'recipe')
            is_valid = False
        if len(recipe_data['instructions']) < 3:
            flash('Instructions must be 4 characters or more.', 'recipe')
            is_valid = False
        #wasn't sure how to do this before this assignment, but this is how I would validate date input and radio (or check box)
        if len(recipe_data['made']) <= 0: #I guess no matter what, something is passed with date input, which is why we check for len
            flash('Date is required!', 'recipe')
            is_valid = False
            #for radio type, something must be interacted with to have it passed through form. So I look for the key in the dictionary.
        if 'under_30' not in recipe_data:
            flash('Please indicate whether under 30 or not!', 'recipe')
            is_valid = False
        return is_valid
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
    
    @classmethod
    def get_all_recipes_with_creator(cls):
        query = "SELECT * FROM recipes JOIN users on recipes.user_id = users.id;"
        results = connectToMySQL('recipes').query_db(query)
        all_recipes = []
        for x in results:
            one_recipe = cls(x)
            one_recipes_creator_info = {
                "id": x['users.id'],
                "first_name":x['first_name'],
                "last_name":x['last_name'],
                "email": x['email'],
                "password":x['password'],
                "created_at":x['users.created_at'],
                "updated_at":x['users.updated_at']
                }
            author = User(one_recipes_creator_info)
            one_recipe.creator = author
            all_recipes.append(one_recipe)
        return all_recipes

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes').query_db(query)
        recipes = []
        for x in results:
            recipes.append( cls(x) )
        return recipes

    @classmethod
    def get_one_recipe_with_creator(cls,data):
        query = "SELECT * FROM users join recipes ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query,data)
        one_recipe = cls (results[0])
        one_recipe.creator = results[0]["first_name"] + " " + results[0]["last_name"] #creator is usually none, but we update to be the first_name
        print(results[0])
        return one_recipe

    @classmethod
    def save_recipe(cls,data):
        query = "INSERT INTO recipes (name, description,instructions,user_id) VALUES (%(name)s,%(description)s,%(instructions)s,%(user_id)s);"
        return connectToMySQL("recipes").query_db(query,data)

    @classmethod
    def get_one_recipe(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL("recipes").query_db(query,data)
        return cls(results[0])
        
    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s WHERE id= %(id)s;"
        return connectToMySQL('recipes').query_db(query,data)

    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s;"
        return connectToMySQL("recipes").query_db(query,data)


    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters")
        if len(recipe["instructions"]) < 3:
            is_valid= False
            flash("Instructions must be at least 3 characters")
        if len(recipe["description"]) < 3:
            is_valid= False
            flash("Description must be at least 3 characters")
        return is_valid
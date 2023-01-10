from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_app.controllers import users

@app.route('/create_recipe_page')
def create_recipe_page():
    return render_template("addnew.html")

@app.route('/add_new_recipe', methods=['POST'])
def add_new_recipe():
        
    if not Recipe.validate_recipe(request.form):
        return redirect('/create_recipe_page')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "user_id": session['user_id']
    }
    Recipe.save_recipe(data)
    return redirect('/success')

@app.route("/show_recipe/<int:id>")
def show_recipe(id):
    data = {
        "id": id
    }
    user_data = {
        "id": session["user_id"]
    }
    return render_template("recipedesc.html", user= User.get_by_id(user_data), recipes = Recipe.get_one_recipe_with_creator(data))

@app.route("/edit_recipe/<int:id>")
def edit_recipe(id):
    data = {
        "id": id
    }
    user_data = {
        "id": session["user_id"]
    }
    return render_template("editrecipe.html", recipes=Recipe.get_one_recipe(data), user = User.get_by_id(user_data))

@app.route('/update', methods = ["POST"])
def update():
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/edit_recipe/{request.form['id']}")
    data = {
        "name": request.form["name"],
        "instructions": request.form["instructions"],
        "description": request.form["description"],
        "id": request.form["id"]
    }
    Recipe.edit_recipe(data)
    return redirect('/success')

@app.route('/delete_recipe/<int:id>')
def delete_recipe(id):
    data= {
        "id": id
    }
    Recipe.delete_recipe(data)
    return redirect('/success')
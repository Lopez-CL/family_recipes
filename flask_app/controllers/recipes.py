from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# BANNERS
# https: // manytools.org/hacker-tools/ascii-banner/

@app.route("/recipes")
def render_dash():
    if 'user_id' not in session:
        return redirect('/')
    else:
        print(session['user_id'])
        data = {
            'id':session['user_id']
        } #with user id in session I can bring in multiple objects to manipulate in my templates
        return render_template('dashboard.html', this_user = user.User.get_user_by_id(data), all_recipes=recipe.Recipe.show_recipes())

# ROUTES
@app.route('/recipes/new')
def show_rec_page():
    if 'user_id' not in session:
        return redirect('/')
    # data = { I was trying to pass in id num through session but this intial way exposed number to inpsector
    #     'id':session['user_id']
    # }
    return render_template("new_recipes.html",)

@app.route('/add/recipe', methods=['post'])
def add_recipe_db():
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'made': request.form['made'],
        'under_30': request.form['under_30'],
        'user_id': session['user_id']
    }
    recipe.Recipe.save(data)
    return redirect('/recipes')

@app.route('/recipes/<int:id>')
def get_one_user_recipe(id):
    data = {
        'id':id
    }
    user_data = {
        'id':session['user_id']
    }
    return render_template("view_recipe.html", this_recipe=recipe.Recipe.get_recipe_with_user(data), this_user = user.User.get_user_by_id(user_data))

@app.route('/recipes/edit/<int:id>')
def get_recipe(id):
    data = {
        'id': id
    }
    return render_template("edit.html", this_recipe=recipe.Recipe.get_recipe_by_id(data))

@app.route('/edit/recipe/<int:id>', methods=['post'])
def edit_recipe_in_db(id):
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{id}') #allows me to redirect to specific recipe edit page again
    data = { #these data dictionaries in controllers must match in order with how they're written in the model
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'made': request.form['made'],
        'under_30': request.form['under_30'],
        'id': id
    }
    recipe.Recipe.edit_recipe_db(data)
    return redirect ("/recipes")

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    data ={
        "id":id
    }
    recipe.Recipe.delete_recipe_db(data)
    return redirect('/recipes')
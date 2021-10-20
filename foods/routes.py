from foods import app, db
from foods.schemas import *
from foods.models import *

from flask_login import current_user
from flask import session, jsonify, request, make_response, Response
import requests, json, clearbit
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, text
import jwt
import datetime
from functools import wraps
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

clearbit.key='sk_72efbbc8858d259bee2c660da4ca259e'



@app.route("/", methods=["GET"])
def index():
    """A simple function that is only welcome."""
    return jsonify({"Welcome to the food recipes!": ':-)'})


@app.route('/register', methods=['POST'])
def register():
    """This is a function that allows you to create an account on the site."""
    try:
        body= request.get_json()
        user_schema=UserSchema()
        result=user_schema.load(body)

        """Using these two variables(poteuser and potuuser) we can check if \
        the entered email address or username is already in our database.\
         And open a new account based on that."""
        poteuser=User.query.filter_by(email=body['email']).first()
        potuuser=User.query.filter_by(username= body['username']).first()
        if poteuser != None:
            raise ValidationError('Uneli ste Email koji vec postoji u bazi! Napravite nalog preko drugog maila.')
        if potuuser != None:
            raise ValidationError('Uneli ste Username koji vec postoji u bazi! Napravite nalog preko drugog Username_a.')

        url = 'https://api.hunter.io/v2/email-verifier?email=' + body['email']+\
        '&api_key=f424f970109401b732e8f36f5ea1a43c7e79fd15'
        data = requests.get(url)
        data = data.json()


        user=User(email=body['email'],username= body['username'],\
        first_name=body['first_name'], last_name=body['last_name'],\
        password=body['password'],\
        password_hash=generate_password_hash(body['password'], method='sha256'))

        """We will also check if the entered email address exists \
        and then enter a new user in the database."""
        if data['data']['status']!='invalid':
            db.session.add(user)
            db.session.commit()

            user=user_schema.dump(user)

            return jsonify({"Registracija je uspesna za sledeceg usera":user})
        else:
            raise ValidationError('Uneti email ne postoji!')
    except ValidationError as err:
            return jsonify(err.messages,err.valid_data)


@app.route('/login', methods=['POST'])
def login():
    """This is a function that gives us a token for the required routes."""
    body=request.get_json()

    try:
        login_schema=LoginSchema()
        result=login_schema.load(body)
    except ValidationError as err:
        return jsonify(err.messages,err.valid_data)

    user=User.query.filter_by(username=body['username']).filter_by(password=body['password']).first()
    if user != None:
        expires = datetime.timedelta(days=7)
        access_token= create_access_token(identity=user.id, expires_delta=expires)
        return jsonify({'token': access_token}, 200)
    return 'Uneli ste pogrešno korisničko ime ili lozinku!'

@app.route('/add', methods=['POST'])
@jwt_required()
def add():
    id=get_jwt_identity()
    current_user=User.query.get(id)
    """This is a function that allows you to add a recipe to the database."""
    try:

        body= request.get_json()
        recipe_schema=RecipeSchema()
        result=recipe_schema.load(body)

        """Using these two variables(potnrecipe and pottrecipe) we can check if\
        the entered name or text of recipe is already in our database.\
         And based on that add a new recipe."""
        potnrecipe=Recipe.query.filter_by(name=body['name']).first()
        pottrecipe=Recipe.query.filter_by(recipe_text= body['recipe_text']).first()
        if potnrecipe != None:
            raise ValidationError('Uneli ste naziv recepta koji već postoji u bazi!')
        if pottrecipe != None:
            raise ValidationError('Uneli ste tekst recepta koji već postoji u bazi!')


        recipe= Recipe(name=body['name'], recipe_text=body['recipe_text'],\
        user_id=current_user.id, ingredients=body['ingredients'])
        db.session.add(recipe)
        db.session.commit()

        """By entering the recipe, all the ingredients are entered \
        and assigned to the given recipe."""
        lista=body['ingredients'].split(",")
        for x in lista:
            ingredient=Ingredient(name=x, recipe_id=recipe.id)
            db.session.add(ingredient)
            ingredient.recipe.append(recipe)
        db.session.commit()

        nova_recipe_schema=NovaRecipeSchema()
        recipe=nova_recipe_schema.dump(recipe)

        return jsonify({"Uneti recept je":recipe})
    except ValidationError as err:
            return jsonify(err.messages,err.valid_data)


@app.route('/all', methods=['GET'])
@jwt_required()
def all():
    """This function displays all recipes from the database."""
    id=get_jwt_identity()
    current_user=User.query.get(id)
    try:
        svi= Recipe.query.all()
        nova_recipe_schema=NovaRecipeSchema(many=True)
        svi=nova_recipe_schema.dump(svi)
        return jsonify({"Svi recepti su": svi})
    except ValidationError as err:
            return jsonify(err.messages,err.valid_data)

@app.route('/all_users', methods=['GET'])
def my_users():
    """This function displays all users from the database."""
    try:
        svi=User.query.all()
        nova_user_schema=NovaUserSchema(many=True)
        svi=nova_user_schema.dump(svi)
        return jsonify({"Svi useri su": svi})
    except ValidationError as err:
            return jsonify(err.messages,err.valid_data)

@app.route('/rate', methods=['POST'])
@jwt_required()
def rate():
    """This function is for assigning a recipe rating. \
    It should also be emphasized that the current user cannot \
    rate their own recipe."""
    id=get_jwt_identity()
    current_user=User.query.get(id)
    try:
        body= request.get_json()
        rate_schema=RateSchema()
        result=rate_schema.load(body)

        recipe = Recipe.query.get(body['recipe_id'])
        if recipe != None:
            if current_user.id != recipe.user_id:
                rate=Rate(user_id=current_user.id, ocena=body['ocena'], \
                recipe_id=body['recipe_id'])
                db.session.add(rate)
                db.session.commit()

                nova_rate_schema=NovaRateSchema()
                rate=nova_rate_schema.dump(rate)
                return jsonify({"Ocena je": rate})
            raise ValidationError("Ne možete oceniti sopstveni recept!")
        raise ValidationError("Uneli ste id koji ne odgovara nijednom receptu!")
    except ValidationError as err:
            return jsonify(err.messages,err.valid_data)

@app.route('/prosek',methods=['GET'])
@jwt_required()
def prosek():
    """This is a function that gives us an average rating for each recipe."""
    id=get_jwt_identity()
    current_user=User.query.get(id)
    prosek= db.session.query(Recipe.name, db.func.avg(Rate.ocena)).\
    outerjoin(Rate, Recipe.id==Rate.recipe_id).group_by(Recipe.name).all()

    return jsonify({"Prosečne ocene recepata su":\
    [(f"Naziv recepta: {x[0]}",f"Prosečna ocena je: {x[1]}") for x in prosek]})

@app.route('/najcesci', methods=['GET'])
@jwt_required()
def najcesci():
    """This is a function that gives us 5 the most commonly used recipes, \
    as well as the number of times used."""
    id=get_jwt_identity()
    current_user=User.query.get(id)
    sql = text('SELECT name, COUNT(id) \
    FROM ingredients \
    GROUP BY name \
    ORDER BY COUNT(id) DESC LIMIT 5')
    result = db.engine.execute(sql)
    common = [(f"Naziv sastojka: {ing[0]}", f"Upotrebljen {ing[1]} put")\
    for ing in result]

    return jsonify({"Najčešće korišćeni sastojci su": common})

@app.route('/delete/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    """This function is used to delete the recipe by entering the id. \
    It should also be emphasized that the current user cannot delete \
    someone else's recipe."""
    id_user=get_jwt_identity()
    current_user=User.query.get(id_user)
    try:
        # I nacin za proveru da li je uneti ID INTEGER
        #for i in id:
        #    if ord(i)<=48 or ord(i)>=59:
        #        return 'id mora sadrzati samo brojeve!'
        # II nacin za proveru da li je uneti ID INTEGER
        try:
            par={'id':id}
            id_schema=IdSchema()
            result=id_schema.load(par)
        except ValidationError as err:
                return jsonify(err.messages,err.valid_data)
        recipe=Recipe.query.get(id)
        if recipe != None:
            if current_user.id == recipe.user_id:
                db.session.delete(recipe)
                ingredients=Ingredient.query.filter_by(recipe_id=id).all()
                for i in ingredients:
                    db.session.delete(i)
                db.session.commit()

                nova_recipe_schema=NovaRecipeSchema()
                recipe=nova_recipe_schema.dump(recipe)

                return jsonify({'Izbrisani recept je': recipe})
            raise ValidationError("Ne mozete izbrisati tudji recept!")
        raise ValidationError("Ovaj recept ne postoji!")
    except ValidationError as err:
            return jsonify(err.messages,err.valid_data)

@app.route('/my', methods=['GET'])
@jwt_required()
def my():
    """This function displays all recipes of the current user from the database."""
    id=get_jwt_identity()
    current_user=User.query.get(id)
    try:
        moji=Recipe.query.filter_by(user_id=current_user.id).all()
        recipe_schema=RecipeSchema(many=True)
        moji=recipe_schema.dump(moji)
        return jsonify({'Svi moji recepti su': moji })
    except ValidationError as err:
        return jsonify(err.messages, err.valid_data)

@app.route('/cbit', methods=['GET'])
@jwt_required()
def cbit():
    """This is a function that gives us additional user information \
    based on the email address entered."""
    id=get_jwt_identity()
    current_user=User.query.get(id)
    try:
        body=request.get_json()
        cbit_schema=CbitSchema()
        result=cbit_schema.load(body)

        additional_data = clearbit.Enrichment.find(email=body['email'], stream=True)

        return jsonify({'Dodatne informacije o korisniku': additional_data})
    except ValidationError as err:
        return jsonify(err.messages, err.valid_data)

@app.route('/search_by_name', methods=['GET'])
@jwt_required()
def search_by_name():
    """This is a function that gives us recipes \
    based on the name of the entered recipe."""
    id=get_jwt_identity()
    current_user=User.query.get(id)
    try:
        body=request.get_json()
        name_recipe_schema=NameRecipeSchema()
        result=name_recipe_schema.load(body)

        name=body['name']
        recipe=Recipe.query.filter(Recipe.name.like(f'%{name}%')).all()
        if len(recipe) == 1:
            nova_recipe_schema=NovaRecipeSchema(many=True)
            recipe=nova_recipe_schema.dump(recipe)
            return jsonify({'Recept sa datim nazivom je': recipe})
        elif len(recipe) > 1:
            nova_recipe_schema=NovaRecipeSchema(many=True)
            recipe=nova_recipe_schema.dump(recipe)
            return jsonify({'Recepti sa datim nazivom su': recipe})
        raise ValidationError(f"U bazi nema recepata sa nazivom {body['name']}.")

    except ValidationError as err:
        return jsonify(err.messages, err.valid_data)

@app.route('/search_by_text', methods=['GET'])
@jwt_required()
def search_by_text():
    """This is a function that gives us recipes \
    based on the text of the entered recipe."""
    id=get_jwt_identity()
    current_user=User.query.get(id)
    try:
        body=request.get_json()
        text_recipe_schema=TextRecipeSchema()
        result=text_recipe_schema.load(body)

        recipe_text=body['recipe_text']
        recipe=Recipe.query.filter(Recipe.recipe_text.like(f'%{recipe_text}%')).all()
        if len(recipe) == 1:
            nova_recipe_schema=NovaRecipeSchema(many=True)
            recipe=nova_recipe_schema.dump(recipe)
            return jsonify({'Recept sa datim tekstom je': recipe})
        elif len(recipe) > 1:
            nova_recipe_schema=NovaRecipeSchema(many=True)
            recipe=nova_recipe_schema.dump(recipe)
            return jsonify({'Recepti sa datim tekstom su': recipe})
        raise ValidationError(f"U bazi nema recepata sa tekstom {body['recipe_text']}.")

    except ValidationError as err:
        return jsonify(err.messages, err.valid_data)

@app.route('/search_by_ingredients', methods=['GET'])
@jwt_required()
def search_by_ingredients():
    """This is a function that gives us recipes \
    based on the ingredients of the entered recipe."""
    id=get_jwt_identity()
    current_user=User.query.get(id)
    try:
        body=request.get_json()
        ingredients_recipe_schema=IngredientsRecipeSchema()
        result=ingredients_recipe_schema.load(body)

        ingredients=body['ingredients']
        recipe=Recipe.query.filter(Recipe.ingredients.like(f'%{ingredients}%')).all()
        if len(recipe) == 1:
            nova_recipe_schema=NovaRecipeSchema(many=True)
            recipe=nova_recipe_schema.dump(recipe)
            return jsonify({'Recept sa unetim sastojcima je': recipe})
        elif len(recipe) > 1:
            nova_recipe_schema=NovaRecipeSchema(many=True)
            recipe=nova_recipe_schema.dump(recipe)
            return jsonify({'Recepti sa unetim sastojcima su': recipe})
        raise ValidationError(f"U bazi nema recepata sa sastojkom {body['ingredients']}.")

    except ValidationError as err:
        return jsonify(err.messages, err.valid_data)

@app.route('/min_ingredients', methods=['GET'])
@jwt_required()
def min_ingredients():
    """This is a function that gives us the name of the recipe \
    with the minimum number of ingredients, \
    as well as the number of ingredients for that recipe."""
    id=get_jwt_identity()
    current_user=User.query.get(id)

    sql = text('SELECT recipes.name, COUNT(ingredients.id) \
    FROM recipes INNER JOIN ingredients \
      ON ingredients.recipe_id = recipes.id \
    GROUP BY recipes.name \
    HAVING COUNT(ingredients.id) > 0 \
    ORDER BY COUNT(ingredients.id) ASC LIMIT 1')
    result = db.engine.execute(sql)
    recmin = [(f"Naziv recepta: {rec[0]}", f"Broj sastojaka recepta: {rec[1]}")\
    for rec in result]
    return jsonify({'Recept sa najmanjim brojem sastojaka je ': recmin})

@app.route('/max_ingredients', methods=['GET'])
@jwt_required()
def max_ingredients():
    """This is a function that gives us the name of the recipe \
    with the maximum number of ingredients, \
    as well as the number of ingredients for that recipe."""
    id=get_jwt_identity()
    current_user=User.query.get(id)

    sql = text('SELECT recipes.name, COUNT(ingredients.id) \
    FROM recipes INNER JOIN ingredients \
      ON ingredients.recipe_id = recipes.id \
    GROUP BY recipes.name \
    HAVING COUNT(ingredients.id) > 0 \
    ORDER BY COUNT(ingredients.id) DESC LIMIT 1')
    result = db.engine.execute(sql)
    recmax = [(f"Naziv recepta: {rec[0]}", f"Broj sastojaka recepta: {rec[1]}")\
    for rec in result]
    return jsonify({'Recept sa najvecim brojem sastojaka je ': recmax})

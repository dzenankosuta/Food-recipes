from marshmallow import Schema, fields, post_load
from marshmallow import ValidationError, validates, validate


class UserSchema(Schema):
    first_name=fields.String(required=True)
    last_name=fields.String(required=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)

    @validates('first_name')
    def validate_first_name(self,first_name):
        if first_name == '':
            raise ValidationError("Morate uneti svoje ime!")
    @validates('last_name')
    def validate_last_name(self,last_name):
        if last_name == '':
            raise ValidationError("Morate uneti svoje prezime!")
    @validates('username')
    def validate_username(self,username):
        if username == '':
            raise ValidationError("Morate uneti svoj username!")
    @validates('password')
    def validate_password(self,password):
        if password == '':
            raise ValidationError("Morate uneti lozinku!")

class NovaUserSchema(Schema):

    id=fields.Integer(required=True)
    first_name=fields.String(required=True)
    last_name=fields.String(required=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password_hash = fields.String(required=True)

class RateSchema(Schema):
    ocena=fields.Integer(required=True)
    recipe_id=fields.Integer(required=True)

    @validates('ocena')
    def validate_ocena(self,ocena):
        if ocena > 5 or ocena < 1:
            raise ValidationError("Ocena mora biti od 1 do 5!")

class NovaRateSchema(Schema):
    ocena=fields.Integer(required=True)
    recipe_id=fields.Integer(required=True)
    user_id=fields.Integer(required=True)

class RecipeSchema(Schema):
    name = fields.String(required=True)
    ingredients= fields.String(required=True)
    recipe_text=fields.String(required=True)

    @validates('name')
    def validate_name(self,name):
        if name == '':
            raise ValidationError("Ime recepta ne sme biti prazno!")
    @validates('ingredients')
    def validate_ingredients(self,ingredients):
        if ingredients == '':
            raise ValidationError("Morate uneti sastojke za dati recept!")
    @validates('recipe_text')
    def validate_recipe_text(self,recipe_text):
        if recipe_text == '':
            raise ValidationError("Tekst recepta mora biti popunjen!")

class NameRecipeSchema(Schema):
    name = fields.String(required=True)

    @validates('name')
    def validate_name(self,name):
        if name == '':
            raise ValidationError("Ime recepta ne sme biti prazno!")

class TextRecipeSchema(Schema):
    recipe_text = fields.String(required=True)

    @validates('recipe_text')
    def validate_recipe_text(self,recipe_text):
        if recipe_text == '':
            raise ValidationError("Tekst recepta mora biti popunjen!")

class IngredientsRecipeSchema(Schema):
    ingredients = fields.String(required=True)

    @validates('ingredients')
    def validate_ingredients(self,ingredients):
        if ingredients == '' or ingredients == ',':
            raise ValidationError("Morate uneti sastojke za dati recept!")


class NovaRecipeSchema(Schema):
    id=fields.Integer(required=True)
    name = fields.String(required=True)
    ingredients= fields.String(required=True)
    recipe_text=fields.String(required=True)


class  IngredientSchema(Schema):
    name = fields.String(required=True)
    recipe_id=fields.Integer(required=True)

class IdSchema(Schema):
    id=fields.Integer(required=True)

class CbitSchema(Schema):
    email=fields.Email(required=True)

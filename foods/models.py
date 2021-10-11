from foods import db
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash,check_password_hash



user_rat= db.Table('user_rat',
db.Column('rates_id', db.Integer, db.ForeignKey('rates.id', ondelete='CASCADE'),\
primary_key=True),
db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'),\
primary_key=True)
)


rec_ing= db.Table('rec_ing',
db.Column('ingredient_id', db.Integer, \
db.ForeignKey('ingredients.id', ondelete='CASCADE'),  primary_key=True),
db.Column('recipe_id', db.Integer,\
db.ForeignKey('recipes.id', ondelete='CASCADE'),  primary_key=True)
)




rec_rat= db.Table('rec_rat',
db.Column('rates_id', db.Integer, \
db.ForeignKey('rates.id', ondelete='CASCADE'),primary_key=True),
db.Column('recipe_id', db.Integer, \
db.ForeignKey('recipes.id', ondelete='CASCADE'),primary_key=True)
)


class User(db.Model, UserMixin):
    __tablename__='users'

    id= db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(64), unique=True, index=True, nullable=False)
    username=db.Column(db.String(64),unique=True, nullable=False)
    first_name=db.Column(db.String(64), nullable=False)
    last_name=db.Column(db.String(64), nullable=False)
    password= db.Column(db.String(128), nullable=False)
    password_hash= db.Column(db.String(128))
    recipes = db.relationship('Recipe', backref='user', lazy='dynamic', \
    cascade="all, delete", passive_deletes=True)
    rates= db.relationship('Rate',secondary=user_rat, \
    backref=db.backref('user',lazy='dynamic'), cascade="all, delete", passive_deletes=True)


    def __init__(self,email,username,first_name,last_name,password,password_hash):
        self.email=email
        self.username=username
        self.first_name=first_name
        self.last_name=last_name
        self.password=password
        self.password_hash= generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


class Rate(db.Model,UserMixin):
    __tablename__='rates'

    id= db.Column(db.Integer, primary_key=True)
    ocena=db.Column(db.Integer, index=True, nullable=False)
    recipe_id = db.Column(db.Integer, \
    db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __init__(self,user_id,ocena, recipe_id):
        self.user_id=user_id
        self.ocena=ocena
        self.recipe_id=recipe_id


class Recipe(db.Model, UserMixin):
    __tablename__='recipes'

    id= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(64), unique=True, index=True, nullable=False)
    recipe_text=db.Column(db.String(128), unique=True, index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    ingredients=db.Column(db.String(64), index=True, nullable=False)
    veza_sa_ing= db.relationship('Ingredient',secondary=rec_ing, \
    backref=db.backref('recipe',lazy='dynamic'), cascade="all, delete", passive_deletes=True)
    rates= db.relationship('Rate',secondary=rec_rat, \
    backref=db.backref('recipe',lazy='dynamic'), cascade="all, delete", passive_deletes=True)

    def __init__(self,name,recipe_text,user_id,ingredients):
        self.name=name
        self.user_id=user_id
        self.ingredients=ingredients
        self.recipe_text=recipe_text


class Ingredient(db.Model, UserMixin):
    __tablename__='ingredients'

    id= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(64), index=True, nullable=False)
    recipe_id = db.Column(db.Integer, \
    db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)

    def __init__(self,name,recipe_id):
        self.name=name
        self.recipe_id=recipe_id

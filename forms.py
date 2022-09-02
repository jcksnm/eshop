from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class AddForm(FlaskForm):
    email = StringField("Email Address:")
    username = StringField("Username:")
    password = StringField("Password:")
    submit = SubmitField("Sign Up")

class CheckForms(FlaskForm):
    username = StringField("Email:")
    password = StringField("Password:")
    submit = SubmitField("Sign Up")

class ManagerForms(FlaskForm):
    username = StringField("Email:")
    password = StringField("Password:")
    email = StringField("Email:")
    manager = StringField("Managerial Status:")
    add_item = StringField("Add Inventory Item:")
    delete_item = StringField("Delete Inventory Item:")
    submit = SubmitField("Sign Up")

class SearchForm(FlaskForm):
    search = StringField("Search our inventory...")
    submit = SubmitField("Search")

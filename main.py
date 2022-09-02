from decimal import ROUND_HALF_DOWN
from operator import inv
import os
from re import L

from forms import AddForm, CheckForms, ManagerForms, SearchForm
from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

quant = 0

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    status = db.Column(db.Integer)
    manager = db.Column(db.Integer)

    def __init__(self, email, username, password, status, manager):

        self.email = email
        self.username = username
        self.password = password
        self.status = status
        self.manager = manager

    def __repr__(self):
        return f"Email: {self.email}, Username: {self.username}, Password: {self.password}, Status: {self.status}, Manager: {self.manager}, Cart: {self.cart}"

class Item(db.Model):
    
    tablename__ = 'items'                        
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.Text)
    item_price = db.Column(db.Text)
    item_quantity = db.Column(db.Text)

    def __init__(self, item_name, item_price, item_quantity):

        self.item_name = item_name
        self.item_price = item_price
        self.item_quantity = item_quantity

    def __repr__(self):
        return f"Item: {self.item_name}, Price: {self.item_price}, Quantity: {self.item_quantity}"

class Cart(db.Model):
    tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.Text)
    item_price = db.Column(db.Text)
    item_quantity = db.Column(db.Text)

    def __init__(self, item_name, item_price, item_quantity):

        self.item_name = item_name
        self.item_price = item_price
        self.item_quantity = item_quantity
        
@app.route('/', methods=['GET','POST'])
def index():
    check_form = CheckForms()
    if request.method == 'POST':
        click = request.form['cart']
        if click == '[add galaxy to cart]':
            galaxy = Cart('Galaxy', '$800', '1')
            db.session.add(galaxy)
            db.session.commit()
        if click == '[add beats to cart]':
            beats = Cart('Beats', '$150', '1')
            db.session.add(beats)
            db.session.commit()
        if click == '[add arduino to cart]':
            arduino = Cart('Arduino', '$100', '1')
            db.session.add(arduino)
            db.session.commit()
    return render_template('home.html')

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['pass']
        emailid = request.form['emailid']
        user_data = User(email, username, password, 0, 0)
        db.session.add(user_data)
        db.session.commit()
        return render_template('thankYou.html')
    return render_template('signUp.html')

@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['pass']
        role = request.form['user']
        paspw = db.session.query(User.password,User.manager).filter(User.username == username, User.manager == role ).all()
        if(len(paspw) >= 1):
            if((paspw[0][0] == password )):
                if(int(role) == paspw[0][1]):
                    if(int(role) == 1):
                        return render_template('managerPage.html')
                    elif(int(role) == 0):
                        return render_template('home.html')
            else:
                return render_template('signin.html')

    return render_template("signin.html")

@app.route('/cart')
def cart():
    oo= db.session.query(Cart, 
                         func.count(Cart.item_name)).group_by(Cart.item_name).all()
    return render_template("cart.html", cart= oo)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    user_search = Item.query
    searched_item = []
    not_found = "Sorry, item not found..."
    global item
    item = form.search.data
    if form.validate_on_submit():
        user_search = user_search.filter(Item.item_name.like('%' + form.search.data + '%'))
        user_search = user_search.order_by(Item.item_name).all()
        searched_item.append(user_search)
        return render_template('founditem.html', searched_item=searched_item, not_found=not_found)
    return render_template('search.html', form=form, searched_item=searched_item)

@app.route('/additemtocart', methods=['GET', 'POST'])
def additemtocart():
    if item == "Galaxy":
        price = "$700"
    if item == "Beats":
        price = "$150"
    if item == "Arduino":
        price = "$100"
    add_to_cart =  Cart(item,price,'1')
    db.session.add(add_to_cart)
    db.session.commit()
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)

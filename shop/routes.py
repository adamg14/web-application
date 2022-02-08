from flask import render_template, flash, redirect, url_for
from flask.globals import request
from shop import app, db
from shop.forms import LoginForm, RegistrationForm
from shop.models import User, Product, ShoppingBasket
from flask_login import current_user, login_user, logout_user, login_required
from shop.models import User



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if the user is already logged in 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # if the user does not exist or the password doesn't match
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/product', methods=['GET'])
@login_required
def product():
    sort_value = request.args.get("sort")
    print(len(request.args))
    if sort_value == "price":
        products = Product.query.order_by(Product.price)
    elif sort_value == "alphabetical order":
        products = Product.query.order_by(Product.product_name)
    elif sort_value == "weight":
        products = Product.query.order_by(Product.weight)
    else:
        products = Product.query.all()
    return render_template('product.html', products=products, sort_value=sort_value)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have created an account. You can now login.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/product/<product_name>')
@login_required
def product_page(product_name):
    product = Product.query.filter_by(product_name=product_name).first_or_404()
    return render_template('product_page.html', product=product)

@app.route('/addtobasket', methods=['POST'])
@login_required
def addtobasket(): 
    productID = request.form.get("productID")
    userID = int(current_user.id)
    shoppingbasket = ShoppingBasket(user_id=userID, product_id=productID)
    db.session.add(shoppingbasket)
    db.session.commit()
    products = Product.query.all()
    flash('item added to your shopping basket')
    return render_template('product.html', products=products)

        
@app.route('/shoppingbasket')
@login_required
def shoppingbasket():
    # this list needs to be replaced with a SQL query
    customer = int(current_user.id)
    items = ShoppingBasket.query.filter_by(user_id=customer)
    total = 0
    for item in items:
        total += item.product.price
    return render_template('shoppingbasket.html', items=items, total=total)


@app.route('/checkout')
@login_required
def checkout():
    return render_template('checkout.html')


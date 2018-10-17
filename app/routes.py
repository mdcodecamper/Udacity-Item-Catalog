from app import app 
from app import db
from flask import render_template, flash, url_for, redirect, request
from app.forms import LoginForm, RegistrationForm, CategoryForm
from app.models import User, Category, Item
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    
    catalogs = [
        {
            'name': 'Soccer',
            'description': 'Popular game in Europe!'
        },
        {
            'name': 'Cricket',
            'description': 'Popular game in Asia!'
        }
    ]
    return render_template('index.html', title = 'Home Page', catalogs=catalogs)

## =============================  Login Management System ==================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


## =============================  Category Module ==================================

@app.route('/category/new', methods=['GET', 'POST'])
def addCategory():
    if current_user.is_authenticated:
        categories = Category.query.all()
        form = CategoryForm()
        if form.validate_on_submit():
            category = Category(name=form.name.data, description=form.description.data)
            db.session.add(category)
            db.session.commit()
            flash('Successfully Added the Category!')
            return redirect(url_for('category'))
        elif form.cancel.data == True:
            return redirect(url_for('category'))
    return render_template('addCategory.html', title='Add Category', form=form)


@app.route('/category/', methods=['GET'])
def category():
    if current_user.is_authenticated:
        categories = Category.query.all()
        return render_template('categoryList.html', categories = categories)
    return redirect(url_for('login'))

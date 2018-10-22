from app import app 
from app import db
from flask import render_template, flash, url_for, redirect, request
from app.forms import LoginForm, RegistrationForm, CategoryForm, EditCategoryForm, DeleteCategoryForm, ItemForm
from app.models import User, Category, Item
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = 'Home Page')

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
    return render_template('auth/register.html', title='Register', form=form)



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
    return render_template('auth/login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


## =============================  Category Module ==================================
@app.route('/catalog/categories', methods=['GET'])
def category():
    categories = Category.query.all()
    return render_template('category/categoryList.html', categories = categories)


@app.route('/catalog/category-latest', methods=['GET'])
def categoryLatest():
    categories = Category.query.all()
    return render_template('category/categoryLatest.html', categories = categories)
    

@app.route('/catalog/category/new', methods=['GET', 'POST'])
@login_required
def addCategory():
    if current_user.is_authenticated:
        form = CategoryForm()
        hasCategory = Category.query.filter_by(name=form.name.data).first()
        if hasCategory is not None:
            flash('Category is already exists.')
            return render_template('category/addCategory.html', title='Add Category', form=form)

        if form.validate_on_submit():
            category = Category(name=form.name.data, description=form.description.data)
            db.session.add(category)
            db.session.commit()
            flash('Successfully Added the Category!')
            return redirect(url_for('category'))
        elif form.cancel.data == True:
            return redirect(url_for('category'))
    return render_template('category/addCategory.html', title='Add Category', form=form)



@app.route('/catalog/category/<string:category_name>/edit', methods=['GET', 'POST'])
@login_required
def editCategory(category_name):
    if current_user.is_authenticated:
        editedCategory = Category.query.filter_by(name=category_name).first()
        form = EditCategoryForm()
        if form.validate_on_submit():
            if request.form['name']:
                editedCategory.name = form.name.data
            if request.form['description']:    
                editedCategory.description = form.description.data
            db.session.add(editedCategory)
            db.session.commit()
            flash('Successfully Edited the Category!')
            return redirect(url_for('category'))
    return render_template('category/editCategory.html', title='Edit Category', editedCategory=editedCategory, category_name=editedCategory.name, form=form)


@app.route('/catalog/category/<string:category_name>/delete', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_name):
    if current_user.is_authenticated:
        categoryToDelete = Category.query.filter_by(name=category_name).first()
        db.session.delete(categoryToDelete)
        db.session.commit()
        flash('Successfully Deleted the Category!')
        return redirect(url_for('category'))
    return render_template('category/deleteCategory.html', title='Delete Category', categoryToDelete = categoryToDelete)
        


## =============================  Item Module ==================================

@app.route('/catalog/<int:category_id>/items', methods=['GET'])
def item(category_id):
    categories = Category.query.all()
    category = Category.query.filter_by(id=category_id).one()
    items = Item.query.filter_by(id=category.id).all()
    return render_template('item/itemList.html', items= items, categories=categories, category = category)
    

@app.route('/catalog/<int:category_id>/items/<int:item_id>', methods=['GET'])
def itemDetails(category_id, item_id):
    category = Category.query.filter_by(id=category_id).one()
    items = Item.query.filter_by(id=category.id).all()
    return render_template('item/itemDetails.html', category = category, items= items)
    

@app.route('/catalog/<int:category_id>/item/new', methods=['GET', 'POST'])
@login_required
def addItem(category_id):
    if current_user.is_authenticated:
        category = Category.query.filter_by(id=category_id).one()
        form = ItemForm()
        if form.validate_on_submit():
            item = Item(title=form.name.data, description=form.description.data, category_id=category.id)
            db.session.add(item)
            db.session.commit()
            flash('Successfully Added the Item!')
            return redirect(url_for('item', category_id=category_id))
        elif form.cancel.data == True:
            return redirect(url_for('item', category_id=category_id))
    return render_template('item/addItem.html', title='Add Item', form=form, category=category)


@app.route('/catalog/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def editItem(category_id, item_id):
    if current_user.is_authenticated:
        category = Category.query.filter_by(id=category_id).first()
        editedItem = Item.query.filter_by(category_id=category.id).one()
        form = ItemForm()
        if form.validate_on_submit():
            if request.form['name']:
                editedItem.title = form.name.data
            if request.form['description']:    
                editedItem.description = form.description.data
            db.session.add(editedItem)
            db.session.commit()
            flash('Successfully Edited the Item!')
            return redirect(url_for('item', category_id=category_id))
    return render_template('item/editItem.html', title='Edit Item', editedItem=editedItem, category_id=category.id, form=form)


@app.route('/catalog/<int:category_id>/<int:item_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(category_id, item_id):
    if current_user.is_authenticated:
        category = Category.query.filter_by(id=category_id).first()
        itemToDelete = Item.query.filter_by(category_id=category.id).one()
        db.session.delete(itemToDelete)
        db.session.commit()
        flash('Successfully Deleted the Item!')
        return redirect(url_for('item', category_id=category_id))
    return render_template('item/deleteItem.html', title='Delete Item', itemToDelete = itemToDelete)
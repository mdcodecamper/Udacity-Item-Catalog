from app import app
from flask import render_template, flash
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Saney'}
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
    return render_template('index.html', title = 'Home Page', user=user, catalogs=catalogs)

## =============================  Login Management System ==================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for User: {}'.format(form.username.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

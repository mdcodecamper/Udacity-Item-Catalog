from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms.validators import DataRequired
from app.models import User, Category


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Add ')
    cancel = SubmitField('Cancel ')
  
    def validate_category_name(self, name):
        category = Category.query.filter_by(category=name.data).first()
        if category is not None:
            raise ValidationError('This category is already exist!!!')




class EditCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description',  validators=[Length(min=0, max=256)])
    submit = SubmitField('Edit ')


class DeleteCategoryForm(FlaskForm):
    submit = SubmitField('Delete ')


class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Add ')
    cancel = SubmitField('Cancel ')
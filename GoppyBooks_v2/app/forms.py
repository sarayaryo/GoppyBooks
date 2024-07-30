from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app.models import User

class LoginForm(FlaskForm):
    name = SelectField('Name', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Register')

class BorrowForm(FlaskForm):
    book_id = IntegerField('Book ID', validators=[DataRequired()])
    submit = SubmitField('Borrow')

class ReturnForm(FlaskForm):
    book_id = IntegerField('Book ID', validators=[DataRequired()])
    submit = SubmitField('Return')

class SearchForm(FlaskForm):
    search_query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Book, Borrow
from app.forms import LoginForm, RegistrationForm, BorrowForm, ReturnForm, SearchForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user:
            login_user(user)
            return redirect(url_for('main.mypage'))
        else:
            flash('Login Unsuccessful. Please check name and try again.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/mypage')
@login_required
def mypage():
    borrowed_books = Borrow.query.filter_by(user_id=current_user.id, return_date=None).all()
    return render_template('mypage.html', borrowed_books=borrowed_books)

@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        search_query = form.search_query.data
        search_results = Book.query.filter(
            (Book.title.contains(search_query)) | 
            (Book.authors.contains(search_query)) | 
            (Book.description.contains(search_query))
        ).all()
        return render_template('search_results.html', search_results=search_results)
    return render_template('search.html', form=form)

@main.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow(book_id):
    book = Book.query.get_or_404(book_id)
    if not book.is_borrowed:
        borrow = Borrow(book_id=book.id, user_id=current_user.id)
        book.is_borrowed = True
        db.session.add(borrow)
        db.session.commit()
        flash('Book borrowed successfully', 'success')
    else:
        flash('Book is not available', 'danger')
    return redirect(url_for('main.mypage'))

@main.route('/return', methods=['GET', 'POST'])
@login_required
def return_book():
    form = ReturnForm()
    if form.validate_on_submit():
        borrow = Borrow.query.filter_by(book_id=form.book_id.data, user_id=current_user.id).first()
        if borrow and borrow.return_date is None:
            borrow.return_date = datetime.utcnow()
            book = Book.query.filter_by(id=borrow.book_id).first()
            book.is_borrowed = False
            db.session.commit()
            flash('Book returned successfully', 'success')
        else:
            flash('Invalid return attempt', 'danger')
    return render_template('return.html', form=form)
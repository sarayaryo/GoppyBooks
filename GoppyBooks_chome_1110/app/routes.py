from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Book, Borrow
from app.forms import LoginForm, RegistrationForm, BorrowForm, ReturnForm, SearchForm
import logging
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    form.name.choices = [(user.id, user.name) for user in User.query.all()]
    if form.validate_on_submit():
        user = User.query.get(form.name.data)
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
    try:
        book = Book.query.get_or_404(book_id)
        if not book.is_borrowed:
            borrow = Borrow(book_id=book.id, user_id=current_user.id)
            book.is_borrowed = True
            current_user.current_borrowed_book_id = book.id
            db.session.add(borrow)
            db.session.commit()
            flash('Book borrowed successfully', 'success')
        else:
            flash('Book is not available', 'danger')
    except Exception as e:
        logging.error(f"Error borrowing book: {e}")
        flash('An error occurred while borrowing the book.', 'danger')
    return redirect(url_for('main.mypage'))

@main.route('/return/<int:borrow_id>', methods=['POST'])
@login_required
def return_book(borrow_id):
    try:
        borrow = Borrow.query.get_or_404(borrow_id)
        if borrow.return_date is None:
            borrow.return_date = datetime.utcnow()
            book = Book.query.filter_by(id=borrow.book_id).first()
            book.is_borrowed = False
            current_user.current_borrowed_book_id = None
            db.session.commit()
            flash('Book returned successfully', 'success')
        else:
            flash('Invalid return attempt', 'danger')
    except Exception as e:
        logging.error(f"Error returning book: {e}")
        flash('An error occurred while returning the book.', 'danger')
    return redirect(url_for('main.mypage'))

@main.route('/book/<int:book_id>', methods=['GET'])
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)  # 該当する本を取得。見つからない場合は404エラー
    return render_template('book_detail.html', book=book)

@main.route('/borrow-history')
def borrow_history():
    histories = Borrow.query.all()
    return render_template('borrow_history.html', histories=histories)

from datetime import datetime
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    borrowed_books = db.relationship('Borrow', back_populates='borrower', lazy=True)
    current_borrowed_book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    authors = db.Column(db.String(200), nullable=False)
    publisher = db.Column(db.String(100))
    published_date = db.Column(db.String(20))
    description = db.Column(db.Text)
    page_count = db.Column(db.Integer)
    categories = db.Column(db.String(100))
    language = db.Column(db.String(20))
    thumbnail = db.Column(db.String(200))
    is_borrowed = db.Column(db.Boolean, default=False)
    borrows = db.relationship('Borrow', back_populates='book', lazy=True, overlaps="borrow_records")

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)
    book = db.relationship('Book', back_populates='borrows', overlaps="borrow_records")
    borrower = db.relationship('User', back_populates='borrowed_books')
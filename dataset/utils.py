
import pandas as pd
import requests
from typing import List, Dict

def search_books(title: str = "", author: str = "", publisher: str = "", max_results: int = 1) -> pd.DataFrame:
    """
    タイトル、著者、出版社で本を検索する関数

    パラメータ:
    title (str): 検索クエリとなるタイトル (デフォルトは空文字)
    author (str): 検索クエリとなる著者 (デフォルトは空文字)
    publisher (str): 検索クエリとなる出版社 (デフォルトは空文字)
    max_results (int): 取得する最大結果数 (デフォルトは1)

    戻り値:
    pd.DataFrame: 検索結果の本のデータフレーム
    """
    query = ""
    if title:
        query += f"+intitle:{title}"
    if author:
        query += f"+inauthor:{author}"
    if publisher:
        query += f"+inpublisher:{publisher}"
    
    if not query:
        raise ValueError("タイトル、著者、出版社のいずれか1つ以上を指定してください。")
    
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={max_results}"
    response = requests.get(url)
    data = response.json()
    
    books: List[Dict[str, str]] = []
    for item in data.get('items', []):
        book_info = item['volumeInfo']
        book = {
            'title': book_info.get('title', ''),
            'authors': ', '.join(book_info.get('authors', [])),
            'publisher': book_info.get('publisher', ''),
            'published_date': book_info.get('publishedDate', ''),
            'description': book_info.get('description', '') + '...' if book_info.get('description') else '',
            'page_count': book_info.get('pageCount', ''),
            'categories': ', '.join(book_info.get('categories', [])),
            'language': book_info.get('language', ''),
            'thumbnail': book_info.get('imageLinks', {}).get('thumbnail', '')
        }
        books.append(book)
    
    return pd.DataFrame(books)

def search_books_by_ISBN(isbn: str, max_results: int = 1) -> pd.DataFrame:
    """
    ISBNで本を検索する関数

    パラメータ:
    isbn (str): 検索クエリとなるISBN
    max_results (int): 取得する最大結果数 (デフォルトは10)

    戻り値:
    pd.DataFrame: 検索結果の本のデータフレーム
    """
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(url)
    data = response.json()
    
    books: List[Dict[str, str]] = []
    for item in data.get('items', []):
        book_info = item['volumeInfo']
        book = {
            'title': book_info.get('title', ''),
            'authors': ', '.join(book_info.get('authors', [])),
            'publisher': book_info.get('publisher', ''),
            'published_date': book_info.get('publishedDate', ''),
            'description': book_info.get('description', '') + '...' if book_info.get('description') else '',
            'page_count': book_info.get('pageCount', ''),
            'categories': ', '.join(book_info.get('categories', [])),
            'language': book_info.get('language', ''),
            'thumbnail': book_info.get('imageLinks', {}).get('thumbnail', '')
        }
        books.append(book)
    
    return pd.DataFrame(books)
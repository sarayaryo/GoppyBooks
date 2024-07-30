import csv
from app import create_app, db
from app.models import Book

app = create_app()

def import_csv_to_db(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            book = Book(
                title=row['title'],
                authors=row['authors'],
                publisher=row['publisher'],
                published_date=row['published_date'],
                description=row['description'],
                page_count=row['page_count'],
                categories=row['categories'],
                language=row['language'],
                thumbnail=row['thumbnail']
            )
            db.session.add(book)
        db.session.commit()

if __name__ == "__main__":
    csv_file_path = 'dataset/dataset_20240623_174106.csv'
    with app.app_context():
        import_csv_to_db(csv_file_path)
import csv
from app import create_app, db
from app.models import User

app = create_app()

def import_users_from_csv(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # print(row)  # デバッグ用に行データを出力
            user = User(name=row['name'])
            db.session.add(user)
        db.session.commit()

if __name__ == "__main__":
    csv_file_path = 'dataset/users.csv'  # ユーザー名リストのCSVファイル
    with app.app_context():
        import_users_from_csv(csv_file_path)
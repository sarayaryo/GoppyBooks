from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# CSVファイルの読み込み
csv_path = os.path.join(os.path.dirname(__file__), 'dataset', 'dataset_20240623_174106.csv')
df = pd.read_csv(csv_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword', '')
    title = request.form.get('title', '')
    authors = request.form.get('authors', '')
    publisher = request.form.get('publisher', '')
    search_type = request.form.get('search_type', 'and')

    # フィルタリング
    if search_type == 'and':
        results = df
        if keyword:
            results = results[results['description'].str.contains(keyword, na=False, case=False)]
        if title:
            results = results[results['title'].str.contains(title, na=False, case=False)]
        if authors:
            results = results[results['authors'].str.contains(authors, na=False, case=False)]
        if publisher:
            results = results[results['publisher'].str.contains(publisher, na=False, case=False)]
    else:  # OR検索
        conditions = []
        if keyword:
            conditions.append(df['description'].str.contains(keyword, na=False, case=False))
        if title:
            conditions.append(df['title'].str.contains(title, na=False, case=False))
        if authors:
            conditions.append(df['authors'].str.contains(authors, na=False, case=False))
        if publisher:
            conditions.append(df['publisher'].str.contains(publisher, na=False, case=False))
        if conditions:
            combined_condition = conditions[0]
            for condition in conditions[1:]:
                combined_condition = combined_condition | condition
            results = df[combined_condition]
        else:
            results = df

    return render_template('results.html', results=results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
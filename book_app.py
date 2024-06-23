from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# CSVファイルの読み込み
df = pd.read_csv('dataset.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = df[df['description'].str.contains(query, na=False, case=False)]
    indices = results.index.tolist()
    return render_template('results.html', indices=indices)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
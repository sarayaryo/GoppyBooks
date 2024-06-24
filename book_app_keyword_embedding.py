from flask import Flask, render_template, request
import pandas as pd
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, models
from sentence_transformers.models import Transformer, Pooling

app = Flask(__name__)

# CSVファイルの読み込み
csv_path = os.path.join(os.path.dirname(__file__), 'dataset', 'dataset_20240623_174106.csv')
df = pd.read_csv(csv_path)

# npyファイルの読み込み
npy_path = os.path.join(os.path.dirname(__file__), 'dataset', 'embeddings_20240625.npy')
embeddings = np.load(npy_path)

# SentenceTransformerモデルの読み込み
transformer = Transformer('cl-tohoku/bert-base-japanese-whole-word-masking')
pooling = Pooling(transformer.get_word_embedding_dimension(), pooling_mode_mean_tokens=False, pooling_mode_cls_token=True, pooling_mode_max_tokens=False)
model = SentenceTransformer(modules=[transformer, pooling])

@app.route('/')
def index():
    return render_template('index_keyword_embedding.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword', '')
    title = request.form.get('title', '')
    authors = request.form.get('authors', '')
    publisher = request.form.get('publisher', '')
    search_type = request.form.get('search_type', 'and')
    query = request.form.get('query', '')
    top_n = int(request.form.get('top_n', 5))

    # キーワード検索
    if keyword or title or authors or publisher:
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
    else:
        results = pd.DataFrame()

    # ベクトル検索
    if query:
        query_embedding = model.encode([query])
        similarities = cosine_similarity(query_embedding, embeddings)[0]
        top_indices = similarities.argsort()[-top_n:][::-1]
        vector_results = df.iloc[top_indices]
    else:
        vector_results = pd.DataFrame()

    return render_template('results_keyword_embedding.html', keyword_results=results.to_dict(orient='records'), vector_results=vector_results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
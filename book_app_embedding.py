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
    return render_template('index_embedding.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '')
    top_n = int(request.form.get('top_n', 5))

    # クエリのembeddingを計算
    query_embedding = model.encode([query])

    # コサイン類似度を計算
    similarities = cosine_similarity(query_embedding, embeddings)[0]

    # 類似度上位n件のインデックスを取得
    top_indices = similarities.argsort()[-top_n:][::-1]

    # インデックスに基づいて結果を取得
    results = df.iloc[top_indices]

    return render_template('results.html', results=results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

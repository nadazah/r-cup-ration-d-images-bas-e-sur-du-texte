from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from flask_cors import CORS
app = Flask(__name__, template_folder='C:/Users/Lenovo-PC/Documents/indp3/atelier1/tp_1')
es = Elasticsearch('http://127.0.0.1:9200')

CORS(app)

index = es.indices.get(index="flickrphoto")
print(index)


@app.route('/')
def home():
    return render_template('search.html')


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    res = es.search(
        index="flickrphoto",
        body={
            "query": {
                "multi_match": {
                    "query": search_term,
                    "fields": [
                        "url",
                        "title",
                        "tags"
                    ],
                    "fuzziness": "1",
                    "prefix_length": 3
                }
            }
        }
    )
    print(res)
    return render_template('results.html', res=res)


if __name__ == '__main__':

    app.run(host='127.0.0.1', port=5000)

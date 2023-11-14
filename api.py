from elasticsearch import Elasticsearch
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Create connection with Elasticsearch
client = Elasticsearch("http://localhost:9200")

def get_movies(query=None):
    body = {
        "query": {
            "match": {
                "title": query
            }
        }
    } if query else {"query": {"match_all": {}}}

    result = client.search(index='movies', body=body)
    return result['hits']['hits']

def get_movie_by_title(title):
    query = {
        "query": {
            "match": {
                "title": title
            }
        }
    }
    result = client.search(index='movies', body=query)
    return result['hits']['hits']

def get_movie_recommendations(title):
    # (unchanged from the previous code)

@app.route('/api/movies/<string:title>', methods=['GET'])
def get_movie(title):
    try:
        movie = get_movie_by_title(title)
        if movie:
            return jsonify(movie)
        else:
            return jsonify({"error": f"Movie with title '{title}' not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/api/recommendations/<string:title>', methods=['GET'])
def get_recommendations(title):
    try:
        recommendations = get_movie_recommendations(title)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search_query', '')
        movies = get_movies(search_query)
    else:
        movies = get_movies()

    return render_template("index.html", movies=movies)

if __name__ == '__main__':
    app.run(debug=True)

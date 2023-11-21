from flask import Flask, render_template, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_movie_info', methods=['GET'])
def get_movie_info():
    title = request.args.get('title')

    if not title:
        return render_template('index.html', error="Title parameter is required")

    # Query to get the input movie information
    query_input_movie = {
        "query": {
            "match": {
                "title.keyword": title
            }
        }
    }

    try:
        # Get information about the input movie
        result_input_movie = es.search(index='user_movies', body=query_input_movie)
        hits_input_movie = result_input_movie['hits']['hits']

        if not hits_input_movie:
            return render_template('index.html', error="Movie not found")

        input_movie_info = hits_input_movie[0]['_source']
        genre = input_movie_info.get("genres_name")[0]

        # Query to get the top 5 similar movies based on the genre

        query_similar_movies = {
            "query": {
                "bool": {
                    "must_not": {
                        "term": {
                            "title.keyword": title
                        }
                    },
                    "filter": [
                        {"term": {"genres_name.keyword": genre}},
                        {"range": {"popularity": {"gte": input_movie_info.get("popularity") - 1, "lte": input_movie_info.get("popularity") + 1}}},
                        {"term": {"original_language.keyword": input_movie_info.get("original_language")}},
                        {"range": {"vote_average": {"gte": input_movie_info.get("vote_average") - 1, "lte": input_movie_info.get("vote_average") + 1}}}
                        
                    ]
                }
            },
            "size": 5,
            "sort": [
                {"popularity": {"order": "desc"}}
            ]
        }

        # Get information about the similar movies
        result_similar_movies = es.search(index='user_movies', body=query_similar_movies)
        hits_similar_movies = result_similar_movies['hits']['hits']

        return render_template('index.html', movie_info=input_movie_info, similar_movies=hits_similar_movies)

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)



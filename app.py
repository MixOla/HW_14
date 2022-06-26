import class_database
from class_database import DataBase
from flask import Flask, jsonify, json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


@app.route('/movie/<title>/')
def get_by_title(title):
    database_res = DataBase('netflix.db')
    result = database_res.get_by_title(title)
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json")


@app.route('/movie/<int:year_1>/to/<int:year_2>/')
def get_by_release_year(year_1, year_2):
    database_res = DataBase('netflix.db')
    return jsonify(database_res.get_by_release_year(year_1, year_2))


@app.route('/rating/<rating>/')
def get_by_rating(rating):
    database_res = DataBase('netflix.db')
    return jsonify(database_res.get_by_rating(rating))

@app.route('/genre/<genre>/')
def get_by_genre(genre):
    database_res = DataBase('netflix.db')
    return jsonify(database_res.get_by_genre(genre))


if __name__ == "__main__":
    app.run(debug=True)


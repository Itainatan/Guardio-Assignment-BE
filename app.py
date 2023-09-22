from flask import Flask, jsonify, request
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)

@app.route('/icon/<name>')
def get_icon_url(name:str):
    return f"https://img.pokemondb.net/sprites/silver/normal/{name}.png"


@app.route('/')
def hello():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 50))

    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    # Validate the page and pageSize values
    if page <= 0 or page_size <= 0:
        return "Invalid page or pageSize", 400

    data = db.get()
    items = data[start_index:end_index]
    return jsonify(items)


if __name__=='__main__':
    app.run(port=8080)
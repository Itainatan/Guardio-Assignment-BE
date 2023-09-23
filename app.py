from flask import Flask, jsonify, request
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)


@app.route("/icon/<name>")
def get_icon_url(name: str):
    return f"https://img.pokemondb.net/sprites/silver/normal/{name}.png"


@app.route("/")
def hello():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("pageSize", 50))
    filters = request.args.getlist("filters")
    sort = request.args.get("sort", None)

    data = db.get()

    filter_conditions = {}

    filtered_data = data

    for filter_str in filters:
        filter_conditions = filter_str.split("&")
        for condition in filter_conditions:
            key, values = condition.split("=")
            values = values.split(",")
            filtered_data = [item for item in filtered_data if item.get(key).lower() in values]

    if sort:
        reverse_sort = sort.lower() == "descending"
        filtered_data.sort(key=lambda item: item.get("number"), reverse=reverse_sort)

    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    # Validate the page and pageSize values
    if page <= 0 or page_size <= 0:
        return "Invalid page or pageSize", 400

    total_length = len(filtered_data)
    paginated_data = filtered_data[start_index:end_index]

    response = {"list": paginated_data, "totalLength": total_length}

    return jsonify(response)


if __name__ == "__main__":
    app.run(port=8080)

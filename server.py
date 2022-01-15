from flask import Flask, render_template, redirect, request, jsonify
from model import connect_to_db
import crud

app = Flask(__name__)

@app.route("/")
def redirect_to_trips():

    return redirect("/trips")


@app.route("/trips")
def render_trips():

    trips = crud.get_all_trips(user_id=1)

    return render_template("trips.html", trips=trips)


@app.route("/trips/<id>")
def render_trip(id):

    trip = crud.get_trip_by_id(id)
    trip_items = crud.get_all_trip_items(id)

    return render_template("trip.html", trip=trip, trip_items=trip_items)


@app.route("/categories")
def render_categories():

    categories = crud.get_all_categories(user_id=1)

    return render_template("categories.html", categories=categories)


@app.route("/category", methods=['POST'])
def add_category_with_rerender():

    name = request.form.get("name")
    crud.create_category(name, 1)

    return redirect("/categories")


@app.route("/api/category", methods=['POST'])
def add_category():

    name = request.get_json().get("name")
    category = crud.create_category(name, 1)

    new_category = {
        "name": category.name,
        "id": category.id,
    }

    return jsonify({"categoryAdded": new_category})


@app.route("/api/edit_category", methods=['POST'])
def edit_category():

    name = request.get_json().get("name")
    id = request.get_json().get("id")

    crud.update_category(id, name)

    return jsonify({"name": name})



@app.route("/items")
def render_items():

    #items = crud.get_all_items(user_id=1)
    #items = crud.get_items_ordered_alphabetically(user_id=1)
    categories = crud.get_all_items_with_categories(user_id=1)

    return render_template("items.html", categories=categories)


@app.route("/templates")
def render_templates():

    templates = crud.get_all_templates(user_id=1)

    return render_template("templates.html", templates=templates)


if __name__ == "__main__":

    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
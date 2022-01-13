from flask import Flask, render_template
from model import connect_to_db
import crud

app = Flask(__name__)

@app.route("/trips")
def render_trips():

    trips = crud.get_all_trips(user_id=1)

    return render_template("trips.html", trips=trips)


@app.route("/categories")
def render_categories():

    categories = crud.get_all_categories(user_id=1)

    return render_template("categories.html", categories=categories)


@app.route("/items")
def render_items():

    items = crud.get_all_items(user_id=1)

    return render_template("items.html", items=items)


@app.route("/templates")
def render_templates():

    templates = crud.get_all_templates(user_id=1)

    return render_template("templates.html", templates=templates)


if __name__ == "__main__":

    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
from flask import Flask, render_template, redirect, request, jsonify
from model import connect_to_db
from datetime import date
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
    
    if not trip.items:
        categories = crud.get_all_categories(user_id=1)
    else:
        categories = crud.get_all_trip_items_with_categories(id)

    return render_template("trip.html", trip=trip, categories=categories)# trip_items=trip_items, items=items


@app.route("/trip", methods=['POST'])
def add_trip_with_rerender():

    name = request.form.get("name")
    str_date = request.form.get("date")
    trip_date = date.fromisoformat(str_date)
    
    crud.create_trip(name, trip_date, user_id=1)
    return redirect("/trips")


@app.route("/<template_id>/trip", methods=['POST'])
def create_trip_with_rerender(template_id):

    name = request.form.get("name")
    str_date = request.form.get("date")
    trip_date = date.fromisoformat(str_date)
    
    trip = crud.create_trip(name, trip_date, user_id=1)
    template = crud.get_template_by_id(template_id)
    
    for item in template.items:
        crud.create_trip_item(item.id, trip.id)

    return redirect(f"/trips/{trip.id}")

@app.route("/categories")
def render_categories():

    categories = crud.get_all_categories(user_id=1)

    return render_template("categories.html", categories=categories)


@app.route("/category", methods=['POST'])
def add_category_with_rerender():

    name = request.form.get("name")
    crud.create_category(name, user_id=1)

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


@app.route("/api/trip_item", methods=['POST'])
def change_checked_trip_item():

    id = request.get_json().get("id")
    status = crud.toggle_checked(id)

    return jsonify({"checkedStatus": status})


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

@app.route("/item", methods=['POST'])
def add_item_with_rerender():

    category_id = request.form.get("category")
    name = request.form.get("name")
    crud.create_item(name, category_id, 1)

    return redirect("/items")


@app.route("/<trip_id>/trip_item", methods=['POST'])
def add_trip_item_with_rerender(trip_id):

    item_id = request.form.get("item")
    quantity = request.form.get("quantity")
    crud.create_trip_item(item_id, trip_id, quantity, False)

    return redirect(f"/trips/{trip_id}")



@app.route("/templates")
def render_templates():

    templates = crud.get_all_templates(user_id=1)

    return render_template("templates.html", templates=templates)


@app.route("/template", methods=['POST'])
def add_template_with_rerender():

    name = request.form.get("name")
    
    crud.create_template(name, user_id=1)
    return redirect("/templates")


@app.route("/templates/<id>")
def render_specific_template(id):

    template = crud.get_template_by_id(id)
    
    if not template.items:
        categories = crud.get_all_categories(user_id=1)
    else:
        categories = crud.get_all_template_items_with_categories(id)
    
    return render_template("template.html", template=template, categories=categories)


@app.route("/<template_id>/template_item", methods=['POST'])
def add_template_item_with_rerender(template_id):

    item_id = request.form.get("item")
    crud.create_template_item(item_id, template_id)

    return redirect(f"/templates/{template_id}")




if __name__ == "__main__":

    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

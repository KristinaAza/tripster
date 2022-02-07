from datetime import date
import hashlib
import os
from flask import Flask, flash, render_template, redirect, request, jsonify, session
from model import connect_to_db
import send_api
import crud

app = Flask(__name__)
app.secret_key=os.environ['SECRET_KEY']

@app.before_request
def redirect_to_login():

    if ("user_id" not in session
            and request.endpoint != "render_login"
            and request.endpoint != "login"):
        return redirect("/login")


@app.route("/login")
def render_login():

    if "user_id" in session:
        return redirect("/trips")

    return render_template("login.html")


@app.route("/users/login", methods=["POST"])
def login():

    form = request.form
    email = form.get("email")
    password = form.get("password")
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    user = crud.get_user_by_email(email)

    if user and password_hash == user.password_hash:
        session["user_id"] = user.id
        return redirect("/trips")
    else:
        flash("Wrong email or password. Try again")
        return redirect("/login")


@app.route("/logout")
def logout():

    session.clear()
    flash("You've successfully logged out")
    return redirect("/login")


@app.route("/")
def redirect_to_trips():

    return redirect("/trips")


@app.route("/trips")
def render_trips():

    user_id = session["user_id"]
    trips = crud.get_all_trips(user_id)

    return render_template("trips.html", trips=trips)


@app.route("/trips/<trip_id>")
def render_trip(trip_id):

    user_id = session["user_id"]
    trip = crud.get_trip_by_id(user_id, trip_id)

    if not trip.items:
        categories = crud.get_all_categories(user_id)
    else:
        categories = crud.get_all_trip_items_with_categories(user_id, trip_id)

    return render_template("trip.html", trip=trip, categories=categories)


@app.route("/api/edit_trip", methods=['POST'])
def edit_trip():

    user_id = session["user_id"]
    trip_id = request.get_json().get("trip_id")
    name = request.get_json().get("name")
    str_date = request.get_json().get("date")
    trip_date = date.fromisoformat(str_date)

    crud.update_trip(user_id, trip_id, name, trip_date)

    return jsonify({"name": name, "trip_date": trip_date})



@app.route("/trip", methods=['POST'])
def add_trip_with_rerender():

    user_id = session["user_id"]
    form = request.form
    name = form.get("name")
    str_date = form.get("date")
    trip_date = date.fromisoformat(str_date)

    crud.create_trip(user_id, name, trip_date)
    return redirect("/trips")


@app.route("/api/trips/delete", methods=['POST'])
def delete_trip():

    user_id = session["user_id"]
    trip_id = request.get_json().get("trip_id")
    crud.delete_trip(trip_id, user_id)

    return jsonify({"status": "trip deleted"})


@app.route("/api/trips/send_email", methods=['POST'])
def send_email():

    user_id = session["user_id"]
    json = request.get_json()
    email = json.get("email")
    trip_id = json.get("trip_id")
    trip = crud.get_trip_by_id(user_id, trip_id)

    subject = f"{trip.name} {trip.trip_date}"
    html_content = f"<h2>{trip.name} {trip.trip_date}</h2><ol>"

    for trip_item in trip.trip_items:
        if trip_item.quantity == 1:
            html_content += f"<li>{trip_item.item.name}</li>"
        else:
            html_content += f"<li>{trip_item.item.name} {trip_item.quantity}</li>"

    html_content +="</ol>"

    send_api.send_email(email, subject, html_content)

    return jsonify({"status": "email sent"})


@app.route("/api/trips/send_sms", methods=['POST'])
def send_sms():

    user_id = session["user_id"]
    json = request.get_json()
    phone_number = json.get("phone_number")
    trip_id = json.get("trip_id")
    trip = crud.get_trip_by_id(user_id, trip_id)

    sms_body = f"{trip.name} {trip.trip_date}\n"

    for i, trip_item in enumerate(trip.trip_items):
        if trip_item.quantity == 1:
            sms_body += f"{i + 1}. {trip_item.item.name}\n"
        else:
            sms_body += f"{i + 1}. {trip_item.item.name} {trip_item.quantity}\n"

    send_api.send_sms(phone_number, sms_body)

    return jsonify({"status": "sms sent"})


@app.route("/<template_id>/trip", methods=['POST'])
def create_trip_with_rerender(template_id):

    user_id = session["user_id"]
    name = request.form.get("name")
    str_date = request.form.get("date")
    trip_date = date.fromisoformat(str_date)

    trip = crud.create_trip(user_id, name, trip_date)
    template = crud.get_template_by_id(user_id, template_id)

    for item in template.items:
        crud.create_trip_item(item.id, trip.id)

    return redirect(f"/trips/{trip.id}")

@app.route("/categories")
def render_categories():

    user_id = session["user_id"]
    categories = crud.get_all_categories(user_id)

    return render_template("categories.html", categories=categories)

@app.route("/categories/<category_id>/delete", methods=['POST'])
def delete_category_with_rerender(category_id):

    user_id = session["user_id"]
    crud.delete_category(category_id, user_id)

    return redirect("/categories")

@app.route("/category", methods=['POST'])
def add_category_with_rerender():

    user_id = session["user_id"]
    name = request.form.get("name")
    crud.create_category(name, user_id)

    return redirect("/categories")


@app.route("/api/categories/delete", methods=['POST'])
def delete_category():

    user_id = session["user_id"]
    category_id = request.get_json().get("category_id")
    crud.delete_category(category_id, user_id)

    return jsonify({"status": "category deleted"})


@app.route("/api/trip_item", methods=['POST'])
def change_checked_trip_item():

    trip_item_id = request.get_json().get("id")
    status = crud.toggle_checked(trip_item_id)

    return jsonify({"checkedStatus": status})


@app.route("/api/edit_category", methods=['POST'])
def edit_category():

    user_id = session["user_id"]
    name = request.get_json().get("name")
    category_id = request.get_json().get("category_id")

    crud.update_category(category_id, name, user_id)

    return jsonify({"name": name})


@app.route("/items")
def render_items():

    user_id = session["user_id"]
    categories = crud.get_all_items_with_categories(user_id)

    return render_template("items.html", categories=categories)


@app.route("/item", methods=['POST'])
def add_item_with_rerender():

    user_id = session["user_id"]
    category_id = request.form.get("category")
    name = request.form.get("name")
    crud.create_item(name, category_id, user_id)

    return redirect("/items")


@app.route("/item/<item_id>/edit", methods=['POST'])
def edit_item_with_rerender(item_id):

    user_id = session["user_id"]
    new_category_id = request.form.get("category")
    new_name = request.form.get("name")
    crud.update_item(item_id, new_category_id, new_name, user_id)

    return redirect("/items")


@app.route("/api/items/delete", methods=['POST'])
def delete_item():

    user_id = session["user_id"]
    item_id = request.get_json().get("item_id")
    crud.delete_item(item_id, user_id)

    return jsonify({"item_id": item_id})


@app.route("/<trip_id>/trip_item", methods=['POST'])
def add_trip_item_with_rerender(trip_id):

    item_id = request.form.get("item")

    if not crud.get_trip_item_by_trip_id_item_id(trip_id, item_id):
        quantity = request.form.get("quantity")
        crud.create_trip_item(item_id, trip_id, quantity, False)

    return redirect(f"/trips/{trip_id}")


@app.route("/trip_items/<trip_item_id>/edit", methods=['POST'])
def edit_trip_item_quantity_with_rerender(trip_item_id):

    quantity = request.form.get("quantity")
    crud.update_trip_item_quantity(trip_item_id, quantity)
    trip_item = crud.get_trip_item_by_id(trip_item_id)

    return redirect(f"/trips/{trip_item.trip_id}")


@app.route("/api/trip_items/delete", methods=['POST'])
def delete_trip_item():

    trip_item_id = request.get_json().get("trip_item_id")
    crud.delete_trip_item(trip_item_id)

    return jsonify({"status": "trip item deleted"})


@app.route("/templates")
def render_templates():

    user_id = session["user_id"]
    templates = crud.get_all_templates(user_id)

    return render_template("templates.html", templates=templates)


@app.route("/api/templates/delete", methods=['POST'])
def delete_template():

    user_id = session["user_id"]
    template_id = request.get_json().get("template_id")
    crud.delete_template(template_id, user_id)

    return jsonify({"status": "template deleted"})



@app.route("/template", methods=['POST'])
def add_template_with_rerender():

    user_id = session["user_id"]
    name = request.form.get("name")

    crud.create_template(name, user_id)
    return redirect("/templates")


@app.route("/api/edit_template", methods=['POST'])
def edit_template():

    user_id = session["user_id"]
    template_id = request.get_json().get("template_id")
    name = request.get_json().get("name")

    crud.update_template(template_id, name, user_id)

    return jsonify({"name": name})


@app.route("/templates/<template_id>")
def render_specific_template(template_id):

    user_id = session["user_id"]
    template = crud.get_template_by_id(user_id, template_id)

    if not template.items:
        categories = crud.get_all_categories(user_id)
    else:
        categories = crud.get_all_template_items_with_categories(user_id, template_id)

    return render_template("template.html", template=template, categories=categories)


@app.route("/<template_id>/template_item", methods=['POST'])
def add_template_item_with_rerender(template_id):

    item_id = request.form.get("item_id")
    crud.create_template_item(item_id, template_id)

    return redirect(f"/templates/{template_id}")


@app.route("/api/template_items/delete", methods=['POST'])
def delete_template_item():

    template_id = request.get_json().get("template_id")
    item_id = request.get_json().get("item_id")
    crud.delete_template_item(template_id, item_id)

    return jsonify({"status": "template item deleted"})


if __name__ == "__main__":

    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    
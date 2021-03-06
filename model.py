"""Tripster app models"""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(50), nullable = False)
    password_hash = db.Column(db.String(64), nullable = False)
    # categories = list of Category objects
    # items = list of Item objects
    # trips = list of Trip objects
    # trip_items= list of TripItem object

    def __repr__(self):
        """Returns descriptive representation for printing"""

        return f"<User id={self.id} email={self.email}>"


class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), nullable = False)
    deleted = db.Column(db.Boolean, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


    # items = list of Item objects

    user = db.relationship("User", backref="categories")

    def __repr__(self):
        """Returns descriptive representation for printing"""

        return f"<Category id={self.id} name={self.name}>"


class Item(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), nullable = False)
    deleted = db.Column(db.Boolean, nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # templates = list of Template objects

    user = db.relationship("User", backref="items")
    category = db.relationship("Category", backref="items")

    def __repr__(self):
        """Returns descriptive representation for printing"""

        return f"<Item id={self.id} name={self.name}>"


class Trip(db.Model):

    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), nullable = False)
    trip_date = db.Column(db.Date, nullable = False)
    deleted = db.Column(db.Boolean, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # trip_items= list of TripItem object

    user = db.relationship("User", backref="trips")
    items = db.relationship("Item", secondary="trip_items", backref="trips")


    def __repr__(self):
        """Returns descriptive representation for printing"""

        return f"<Trip id={self.id} name={self.name}>"


class TripItem(db.Model):

    __tablename__ = "trip_items"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    quantity = db.Column(db.Integer, nullable = False)
    checked = db.Column(db.Boolean, nullable = False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"))

    item = db.relationship("Item", backref="trip_items")
    trip = db.relationship("Trip", backref="trip_items")

    def __repr__(self):
        """Returns descriptive representation for printing"""

        return f"<TripItem id={self.id}>"


class Template(db.Model):

    __tablename__ = "templates"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    deleted = db.Column(db.Boolean, nullable = False)

    user = db.relationship("User", backref="templates")
    items = db.relationship("Item", secondary="template_items", backref="templates")

    def __repr__(self):
        """Returns descriptive representation for printing"""

        return f"<Template id={self.id} name={self.name}>"


class TemplateItem(db.Model):

    __tablename__ = "template_items"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    template_id = db.Column(db.Integer, db.ForeignKey("templates.id"))

    item = db.relationship("Item", backref="template_items")
    template = db.relationship("Template", backref="template_items")

    def __repr__(self):
        """Returns descriptive representation for printing"""

        return f"<TemplateItem id={self.id}>"


def connect_to_db(app, db_uri="postgresql:///tripster", echo=True):

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = echo
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    print("Connected to the db")


def create_test_data():

    Trip.query.filter_by(user_id=1).delete()
    User.query.filter_by(id=1).delete()

    test_user1 = User(id=1, email="test1@test.test", password_hash="1234")
    test_trip1 = Trip(name="SF", trip_date=datetime.date(2011, 11, 11), user_id=1, deleted=False)

    db.session.add_all([test_user1, test_trip1])
    db.session.commit()


if __name__ == "__main__":

    from server import app

    connect_to_db(app)

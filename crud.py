from model import User, Category, Item, Trip, TripItem, Template, TemplateItem, connect_to_db, db

def add_to_db(item):
    db.session.add(item)
    db.session.commit()


# categories
def create_category(name, user_id):

    category = Category(name=name, user_id=user_id)
    add_to_db(category)
    return category

def get_all_categories(user_id):

    categories = Category.query.filter_by(user_id=user_id).all()
    return categories


# items
def create_item(name, category_id, user_id):

    item = Item(name=name, category_id=category_id, user_id=user_id)
    add_to_db(item)
    return item

def get_all_items(user_id):

    items = Item.query.filter_by(user_id=user_id).all()
    return items

# trips
def create_trip(name, trip_date, user_id):

    trip = Trip(name=name, trip_date=trip_date, user_id=user_id)
    add_to_db(trip)
    return trip


def get_all_trips(user_id):

    trips = Trip.query.filter_by(user_id=user_id).all()
    return trips


def get_trip_by_id(id):

    trip = Trip.query.get(id)
    return trip


# trip_items
def create_trip_item(item_id, trip_id, quantity, checked):

    trip_item = TripItem(item_id=item_id, trip_id=trip_id, quantity=quantity, checked=checked)
    add_to_db(trip_item)
    return trip_item


def get_all_trip_items(trip_id):

    trip_items = TripItem.query.filter_by(trip_id=trip_id).all()
    return trip_items


# templates
def create_template(name, user_id):

    template = Template(name=name, user_id=user_id)
    add_to_db(template)
    return template


def get_all_templates(user_id):

    templates = Template.query.filter_by(user_id=user_id).all()
    return templates

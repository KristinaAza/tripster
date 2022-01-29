from model import User, Category, Item, Trip, TripItem, Template, TemplateItem, connect_to_db, db

def add_to_db(item):
    db.session.add(item)
    db.session.commit()


# categories

def create_category(name, user_id):

    category = Category(name=name, user_id=user_id, deleted=False)
    add_to_db(category)
    return category


def update_category(id, name, user_id):

    (
        db.session.query(Category)
        .filter(Category.user_id == user_id)
        .filter(Category.deleted is False)
        .filter(Category.id == id)
        .update({"name": name})
    )
    db.session.commit()

def delete_category(id, user_id):

    (
        db.session.query(Category)
        .filter(Category.user_id == user_id)
        .filter(Category.id == id)
        .update({"deleted": True})
    )
    db.session.commit()


def get_all_categories(user_id):

    categories = (
        Category.query
        .filter_by(user_id=user_id)
        .filter_by(deleted=False)
        .order_by(Category.name).all()
    )
    return categories


# items

def create_item(name, category_id, user_id):

    item = Item(name=name, category_id=category_id, user_id=user_id, deleted=False)
    add_to_db(item)
    return item


def update_item(item_id, category_id, name, user_id):

    (
        db.session.query(Item)
        .filter(user_id == user_id)
        .filter(Item.id == item_id)
        .update({"category_id": category_id, "name": name})
    )
    db.session.commit()


def delete_item(id, user_id):

    (
        db.session.query(Item)
        .filter(Item.user_id == user_id)
        .filter(Item.id == id)
        .update({"deleted": True})
    )
    db.session.commit()


# def get_all_items(user_id):

#     items = Item.query.filter_by(user_id=user_id).all()
#     return items


def get_all_items_with_categories(user_id):

    categories = (
        Category.query.options(db.joinedload("items"))
        .filter_by(user_id=user_id)
        .order_by(Category.name)
        .all()
    )
    return categories


def get_items_ordered_alphabetically(user_id):

    items = Item.query.filter_by(user_id=user_id).order_by('name').all()
    return items


# trips

def create_trip(name, trip_date, user_id):

    trip = Trip(name=name, trip_date=trip_date, user_id=user_id)
    add_to_db(trip)
    return trip


def update_trip(id, name, trip_date, user_id):

    (
        db.session.query(Trip)
        .filter(Trip.user_id == user_id)
        .filter(Trip.id == id)
        .update({"name": name, "trip_date": trip_date})
    )
    db.session.commit()


def get_all_trips(user_id):

    trips = Trip.query.filter_by(user_id=user_id).order_by(Trip.trip_date).all()
    return trips


def get_trip_by_id(id):

    trip = Trip.query.get(id)
    return trip


# trip_items

def create_trip_item(item_id, trip_id, quantity=1, checked=False):

    trip_item = TripItem(item_id=item_id, trip_id=trip_id, quantity=quantity, checked=checked)
    add_to_db(trip_item)
    return trip_item


def get_all_trip_items(trip_id):

    trip_items = TripItem.query.filter_by(trip_id=trip_id).all()
    return trip_items

def get_all_trip_items_with_categories(trip_id):

    categories = (
        Category.query.options(db.joinedload("items")
        .options(db.joinedload("trip_items")))
        .filter(TripItem.trip_id == trip_id)
        .order_by(Category.name)
        .all()
    )
    return categories


def get_trip_item_by_id(id):

    trip_item = TripItem.query.get(id)
    return trip_item


def get_trip_item_by_trip_id_item_id(trip_id, item_id):

    trip_item = (
        TripItem.query
        .filter(TripItem.trip_id == trip_id)
        .filter(TripItem.item_id == item_id)
        .first()
    )
    return trip_item


def toggle_checked(trip_item_id):

    trip_item = get_trip_item_by_id(trip_item_id)
    trip_item.checked = not trip_item.checked
    add_to_db(trip_item)
    return trip_item.checked

# templates

def create_template(name, user_id):

    template = Template(name=name, user_id=user_id)
    add_to_db(template)
    return template


def update_template(id, name, user_id):

    (
        db.session.query(Template)
        .filter(user_id == user_id)
        .filter(Template.id == id)
        .update({"name": name})
    )
    db.session.commit()


def get_all_templates(user_id):

    templates = Template.query.filter_by(user_id=user_id).all()
    return templates


def get_template_by_id(id):

    template = Template.query.get(id)
    return template



# template_items

def create_template_item(item_id, template_id):

    template_item = TemplateItem(item_id=item_id, template_id=template_id)
    add_to_db(template_item)
    return template_item


def get_all_template_items_with_categories(template_id):

    categories = (
        Category.query.options(db.joinedload("items")
        .options(db.joinedload("template_items")))
        .filter(TemplateItem.template_id == template_id)
        .order_by(Category.name)
        .all()
    )
    return categories

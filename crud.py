from model import User, Category, Item, Trip, TripItem, Template, TemplateItem, db

def add_to_db(item):
    db.session.add(item)
    db.session.commit()


# users

def get_user_by_email(email):

    user = User.query.filter(User.email == email).first()
    return user


# categories

def create_category(name, user_id):

    category = Category(name=name, user_id=user_id, deleted=False)
    add_to_db(category)
    return category


def update_category(category_id, name, user_id):

    (
        db.session.query(Category)
        .filter(Category.user_id == user_id)
        .filter(Category.id == category_id)
        .update({"name": name})
    )
    db.session.commit()

def delete_category(category_id, user_id):

    (
        db.session.query(Category)
        .filter(Category.user_id == user_id)
        .filter(Category.id == category_id)
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


def delete_item(item_id, user_id):

    (
        db.session.query(Item)
        .filter(Item.user_id == user_id)
        .filter(Item.id == item_id)
        .update({"deleted": True})
    )
    db.session.commit()


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

def create_trip(user_id, name, trip_date):

    trip = Trip(name=name, trip_date=trip_date, user_id=user_id, deleted=False)
    add_to_db(trip)
    return trip


def update_trip(user_id, trip_id, name, trip_date):

    (
        db.session.query(Trip)
        .filter(Trip.user_id == user_id)
        .filter(Trip.id == trip_id)
        .update({"name": name, "trip_date": trip_date})
    )
    db.session.commit()


def get_all_trips(user_id):

    trips = Trip.query.filter_by(user_id=user_id).order_by(Trip.trip_date.desc()).all()
    return trips


def get_trip_by_id(user_id, trip_id):

    trip = Trip.query.filter(Trip.user_id == user_id).filter(Trip.id == trip_id).first()
    return trip


def delete_trip(trip_id, user_id):

    (
        db.session.query(Trip)
        .filter(Trip.user_id == user_id)
        .filter(Trip.id == trip_id)
        .update({"deleted": True})
    )
    db.session.commit()


# trip_items

def create_trip_item(item_id, trip_id, quantity=1, checked=False):

    trip_item = TripItem(item_id=item_id, trip_id=trip_id, quantity=quantity, checked=checked)
    add_to_db(trip_item)
    return trip_item


def update_trip_item_quantity(trip_item_id, quantity):

    (
        db.session.query(TripItem)
        .filter(TripItem.id == trip_item_id)
        .update({"quantity": quantity})
    )
    db.session.commit()


def get_all_trip_items(trip_id):

    trip_items = TripItem.query.filter_by(trip_id=trip_id).all()
    return trip_items

def get_all_trip_items_with_categories(user_id, trip_id):

    categories = (
        Category.query.options(db.joinedload("items")
        .options(db.joinedload("trip_items")))
        .filter(Category.user_id == user_id)
        .filter(TripItem.trip_id == trip_id)
        .order_by(Category.name)
        .all()
    )
    return categories


def get_trip_item_by_id(trip_item_id):

    trip_item = TripItem.query.get(trip_item_id)
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


def delete_trip_item(trip_item_id):

    TripItem.query.filter_by(id=trip_item_id).delete()
    db.session.commit()


# templates

def create_template(name, user_id):

    template = Template(name=name, user_id=user_id, deleted=False)
    add_to_db(template)
    return template


def update_template(template_id, name, user_id):

    (
        db.session.query(Template)
        .filter(user_id == user_id)
        .filter(Template.id == template_id)
        .update({"name": name})
    )
    db.session.commit()


def delete_template(template_id, user_id):

    (
        db.session.query(Template)
        .filter(Template.user_id == user_id)
        .filter(Template.id == template_id)
        .update({"deleted": True})
    )
    db.session.commit()


def get_all_templates(user_id):

    templates = Template.query.filter_by(user_id=user_id).all()
    return templates


def get_template_by_id(user_id, template_id):

    template = (
        Template.query
        .filter(Template.user_id == user_id)
        .filter(Template.id == template_id)
        .first()
    )
    return template



# template_items

def create_template_item(item_id, template_id):

    template_item = TemplateItem(item_id=item_id, template_id=template_id)
    add_to_db(template_item)
    return template_item


def get_all_template_items_with_categories(user_id, template_id):

    categories = (
        Category.query.options(db.joinedload("items")
        .options(db.joinedload("template_items")))
        .filter(Category.user_id == user_id)
        .filter(TemplateItem.template_id == template_id)
        .order_by(Category.name)
        .all()
    )
    return categories


def delete_template_item(template_id, item_id):

    (
        TemplateItem.query
        .filter((TemplateItem.template_id == template_id) & (TemplateItem.item_id == item_id))
        .delete()
    )
    db.session.commit()

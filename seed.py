import os
import datetime
from model import User, Category, Item, Trip, TripItem, Template, TemplateItem, connect_to_db, db
from server import app

os.system("dropdb tripster")
os.system("createdb tripster")

connect_to_db(app)
db.create_all()


user = User(id=1, email="test@test.test", password_hash="Abc")
category1 = Category(name="Food", user_id=1, deleted=False)
category2 = Category(name="Clothes", user_id=1, deleted=False)
item1 = Item(name="Banana", category_id=1, user_id=1, deleted=False)
item2 = Item(name="Bread", category_id=1, user_id=1, deleted=False)
item3 = Item(name="T-shirt", category_id=2, user_id=1, deleted=False)
item4 = Item(name="Shoes", category_id=2, user_id=1, deleted=False)

trip1 = Trip(name="Yosemite", trip_date=datetime.date(2010, 5, 1), user_id=1)
trip2 = Trip(name="San Diego", trip_date=datetime.date(2020, 10, 2), user_id=1)
trip_item1 = TripItem(quantity=5, checked=False, item_id=1, trip_id=1)
trip1.trip_items.append(trip_item1)
trip_item2 = TripItem(quantity=3, checked=False, item_id=2, trip_id=1)
trip1.trip_items.append(trip_item2)
trip_item3 = TripItem(quantity=1, checked=False, item_id=3, trip_id=1)
trip1.trip_items.append(trip_item3)
trip_item4 = TripItem(quantity=2, checked=False, item_id=4, trip_id=2)
trip2.trip_items.append(trip_item4)


template1 = Template(name="Camping", user_id=1)
template2 = Template(name="Backpacking", user_id=1)
template_item1 = TemplateItem(item_id=1, template_id=1)
template1.template_items.append(template_item1)
template_item2 = TemplateItem(item_id=2, template_id=1)
template1.template_items.append(template_item2)
template_item3 = TemplateItem(item_id=3, template_id=1)
template1.template_items.append(template_item3)
template_item4 = TemplateItem(item_id=4, template_id=2)
template2.template_items.append(template_item4)


db.session.add(user)
db.session.add(category1)
db.session.add(category2)
db.session.add(item1)
db.session.add(item2)
db.session.add(item3)
db.session.add(item4)
db.session.add(trip1)
db.session.add(trip2)
db.session.add(template1)
db.session.add(template2)


db.session.commit()

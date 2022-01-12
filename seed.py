import os
import datetime
from model import User, Category, Item, Trip, TripItem, Template, TemplateItem, connect_to_db, db
from server import app

os.system("dropdb tripster")
os.system("createdb tripster")

connect_to_db(app)
db.create_all()
    

user = User(id=1, email="test@test.test", password_hash="Abc")
category1 = Category(id=1, name="Food", user_id=1)
category2 = Category(id=2, name="Clothes", user_id=1)
item1 = Item(id=1, name="Banana", category_id=1, user_id=1)
item2 = Item(id=2, name="Bread", category_id=1, user_id=1)
item3 = Item(id=3, name="T-shirt", category_id=2, user_id=1)
item4 = Item(id=4, name="Shoes", category_id=2, user_id=1)
trip1 = Trip(id=1, name="Yosemite", trip_date=datetime.date(2010, 5, 1), user_id=1)
trip2 = Trip(id=2, name="San Diego", trip_date=datetime.date(2020, 10, 2), user_id=1)
trip_item = TripItem(id=1, quantity=5, checked=False, item_id=1, trip_id=1)
trip1.trip_items.append(trip_item)

db.session.add(user)
db.session.add(category1)
db.session.add(category2)
db.session.add(item1)
db.session.add(item2)
db.session.add(item3)
db.session.add(item4)
db.session.add(trip1)
db.session.add(trip2)

db.session.commit()
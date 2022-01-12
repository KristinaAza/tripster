from model import User, Category, Item, Trip, TripItem, Template, TemplateItem, connect_to_db

def get_all_trips(user_id):

    trips = Trip.query.filter_by(user_id=user_id).all()

    return trips
from flask import Flask, render_template
from model import connect_to_db
import crud

app = Flask(__name__)

@app.route("/trips")
def render_trips():

    trips = crud.get_all_trips(user_id=1)

    return render_template("trips.html", trips=trips)


if __name__ == "__main__":

    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
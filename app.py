from flask import Flask, render_template, redirect, request, url_for
from models import db, TripPlan, Activity
from datetime import datetime
import random


app = Flask(__name__)

app.config.from_object('config')

with app.app_context():
    db.init_app(app)
    db.create_all()
# This render home page and take random img from web
@app.route('/')
def index():
    random_number = random.randint(1, 1000)
    return render_template('index.html', random_number=random_number)
# This code create new trip and add instance in db
@app.route('/trips/new', methods=['GET', 'POST'])
def create_trip():
    if request.method == 'POST':
        title = request.form['title']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        destination = request.form['destination']
        description = request.form['description']
        new_trip = TripPlan(
            title=title,
            start_date=start_date,
            end_date=end_date,
            destination=destination,
            description=description
        )
        db.session.add(new_trip)
        db.session.commit()

        return redirect(url_for('show_trip', trip_id=new_trip.id))
    
    return render_template('create_trip.html')

@app.route('/trips/<int:trip_id>')
def show_trip(trip_id):
    trip = TripPlan.query.get_or_404(trip_id)
    return render_template('show_trip.html', trip=trip)
@app.route('/trips')
def list_trips():
    trips = TripPlan.query.all()
    return render_template('list_trips.html', trips=trips)
@app.route('/trips/<int:trip_id>/edit', methods=['GET', 'POST'])
def edit_trip(trip_id):
    trip = TripPlan.query.get_or_404(trip_id)

    if request.method == 'POST':
        trip.title = request.form['title']
        trip.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        trip.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        trip.destination = request.form['destination']
        trip.description = request.form['description']
        db.session.commit()
        return redirect(url_for('show_trip', trip_id=trip.id))

    return render_template('edit_trip.html', trip=trip)

@app.route('/trips/<int:trip_id>/delete', methods=['POST'])
def delete_trip(trip_id):
    trip = TripPlan.query.get_or_404(trip_id)
    if request.method == 'POST':
        db.session.delete(trip)
        db.session.commit()
        return redirect(url_for('index')) 
    return render_template('show_trip.html', trip=trip)


# This part is for create edit and delete activities for trip

@app.route('/trips/<int:trip_id>/activities/new', methods=['GET', 'POST'])
def create_activity(trip_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        trip = TripPlan.query.get_or_404(trip_id)
        new_activity = Activity(
            name=name,
            description=description,
            date=date,
            trip_plan=trip
        )
        db.session.add(new_activity)
        db.session.commit()

        return redirect(url_for('display_activities', trip_id=trip_id))
    
    return render_template('create_activity.html', trip_id=trip_id)

@app.route('/trips/<int:trip_id>/activities')
def display_activities(trip_id):
    trip = TripPlan.query.get_or_404(trip_id)
    activities = Activity.query.filter_by(trip_plan_id=trip_id).all()
    return render_template('display_activities.html', trip=trip, activities=activities)

@app.route('/activities/<int:activity_id>/delete', methods=['POST'])
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    db.session.delete(activity)
    db.session.commit()
    if activity:
        return redirect(url_for('display_activities', trip_id=activity.trip_plan_id))
    else:
        return redirect(url_for('show_trip'))

if __name__ == "__main__":
    app.run(debug=True)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Text

db = SQLAlchemy()

class TripPlan(db.Model):
    id = db.mapped_column(db.Integer, primary_key=True)
    title = db.mapped_column(db.String(100), nullable=False)
    start_date = db.mapped_column(db.Date)
    end_date = db.mapped_column(db.Date)
    destination = db.mapped_column(db.String(100))
    description = db.mapped_column(db.Text)
    created_at = db.mapped_column(db.DateTime, default=datetime.utcnow)
    activities = db.relationship('Activity', backref='trip_plan', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"TripPlan(id={self.id}, title={self.title})"

class Activity(db.Model):
    id = db.mapped_column(db.Integer, primary_key=True)
    name = db.mapped_column(db.String(100), nullable=False)
    description = db.mapped_column(db.Text)
    date = db.Column(db.Date)
    trip_plan_id = db.mapped_column(db.Integer, db.ForeignKey('trip_plan.id'), nullable=False)

    def __repr__(self):
        return f"Activity(id={self.id}, name={self.name})"

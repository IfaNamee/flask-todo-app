# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a new Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exercises.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Exercise model
class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(10), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Exercise id={self.id} exercise={self.exercise} duration={self.duration} completed={self.completed} date={self.date}>'

# Initialize the database
with app.app_context():
    db.create_all()

# Home route - Display exercises
@app.route('/')
def index():
    exercises = Exercise.query.order_by(Exercise.date.asc()).all()
    return render_template('index.html', exercises=exercises)

# Route to add a new exercise
@app.route('/add', methods=['POST'])
def add():
    exercise = request.form.get('exercise')  # Fix name to match form
    duration = request.form.get('duration')
    date = request.form.get('date')
    completed = db.Column(db.Boolean, default=False)

    if exercise and duration and date:
        new_exercise = Exercise(exercise=exercise, duration=int(duration), date=date)
        db.session.add(new_exercise)
        db.session.commit()

    return redirect(url_for('index'))

# Route to toggle us an exercise done
@app.route('/toggle/<int:exercise_id>')
def toggle(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    exercise.completed = not exercise.completed
    db.session.commit()
    return redirect(url_for('index'))

# Route to delete an exercise
@app.route('/delete/<int:exercise_id>')
def delete(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    db.session.delete(exercise)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

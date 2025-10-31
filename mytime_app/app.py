from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timesheet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ------------------------
# Database Model
# ------------------------
class Timesheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10))
    location = db.Column(db.String(20))
    hours = db.Column(db.Float)

with app.app_context():
    db.create_all()

# ------------------------
# Routes
# ------------------------

@app.route('/')
def dashboard():
    data = Timesheet.query.all()
    total_hours = sum([d.hours for d in data])
    return render_template('index.html', data=data, total_hours=total_hours)

@app.route('/timesheet')
def timesheet():
    data = Timesheet.query.all()
    return render_template('timesheet.html', data=data)

@app.route('/save', methods=['POST'])
def save():
    records = request.get_json()
    for rec in records:
        existing = Timesheet.query.filter_by(day=rec['day']).first()
        if existing:
            existing.location = rec['location']
            existing.hours = rec['hours']
        else:
            new_entry = Timesheet(day=rec['day'], location=rec['location'], hours=rec['hours'])
            db.session.add(new_entry)
    db.session.commit()
    return jsonify({"status": "success"})

@app.route('/data')
def get_data():
    data = Timesheet.query.all()
    return jsonify([{"day": d.day, "location": d.location, "hours": d.hours} for d in data])

if __name__ == '__main__':
    app.run(debug=True)

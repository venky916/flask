import csv
import os
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db) 

class Students(db.Model):
    __tablename__ = 'Students'
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.Text)
    marks = db.Column(db.Integer)
    def __init__(self, id,name, marks):
        self.id=id
        self.name = name
        self.marks = marks
    def __repr__(self):
        return "Student Name - {} and MRP - {}".format(self.name, self.marks)


@app.route('/')
def show_all():
   return render_template('show_all.html', students = Students.query.all() )

@app.route("/user-by-id/")
def user_by_id():
    id = request.args.get("id")
    result = Students.query.filter_by(id=id).first()
    return render_template("student_id.html", student=result)

@app.route("/user-by-username/<username>")
def user_by_username(username):
    result = Students.query.filter_by(name=username)
    return render_template("show_all.html", students=result)

if __name__ == '__main__':
    with app.app_context():
        with open('data.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                student = Students(id=row['ID'],name=row['Name'],marks=row["Marks"])
                db.session.add(student)
                db.session.commit()
        app.run(debug=True)
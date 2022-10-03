#!/usr/bin/env python3

"""
App Name: 8200dev Course Attendance
Author: Dmitrey Kazin
Purpose: The purpose of this application is to provide
	 is to provide a user-firendly interface for
	 managing students attendance.
"""
# external libraries import
from flask import Flask, render_template, request, redirect, url_for, flash
import secrets

# internal models import
import db
import sftp

# global variables
TEMPALTES_FOLDER = './templates'

app = Flask(__name__, template_folder=TEMPALTES_FOLDER)
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

# tables initialization
@app.before_first_request
def initialization():
    sftp.download_all_csv()
    db.create_temp_attendance()
    db.create_stable_attendance()
    db.create_all_meetings()

# custom err page
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

# stable_attendance tablle presentation
@app.route('/')
def stable_attendance():
    students = db.query_all_stable_attendance()
    return render_template('stable.html', students=students)

# all_meetings table presentation
@app.route('/all')
def all_meetings():
    students = db.query_all_meetings()
    columns = db.query_all_meetings_columns()
    # remove unnecessary stuff from the string
    clean_columns = []
    for i in range (1, len(columns)):
        clean_columns.append(str(columns[i]).split("'")[1])
    return render_template('all_meetings.html', students=students, columns=clean_columns)

# temp_attendance table presentation
@app.route('/temp')
def temp_attendance():
    students = db.query_all_temp_attendance()
    return render_template('temp.html', students=students)

# add a new student to stable_attendance table
@app.route('/add_student', methods=['GET', 'POST'])
def insert():
    if request.method == "GET":
        return render_template('add_student.html')
    if request.method == "POST":
        try:
            name = request.form['name']
            total_min = request.form['total_min']
            total_percentage = request.form['total_percentage']
            db.insert_into_stable_attendance(name, total_min, total_percentage)
            flash('Values inserted successfully.', category='success')
        except:
            flash('Failed to insert values.', category='error')
        finally:
            return redirect(url_for('stable_attendance'))

# delete a student from stable_attendance table
@app.route('/delete/<name>', methods=["GET", "POST"])
def delete(name):
    if request.method == "GET":
        return render_template('delete.html')
    if request.method == "POST":
        try:
            db.delete_stable_student(name)
            flash('Student deleted successfully.', category='success')
        except:
            flash('Failed to delete student.', category='error')
        finally:
            return redirect(url_for('stable_attendance'))

# edit a student from a stable_attendance table
@app.route('/edit/<name>', methods=["GET", "POST"])
def edit(name):
    if request.method == 'GET':
        student = db.query_stable_student(name)
        return render_template('edit.html', student=student)
    if request.method == 'POST':
        try:
            old_name = name
            new_name = request.form['name']
            total_min = request.form['total_min']
            total_percentage = request.form['total_percentage']
            db.edit_stable_student(old_name, new_name, total_min, total_percentage)
            flash('Values modified successfully.', category='success')
        except:
            flash('Failed to modify values.', category='error')
        finally:
            return redirect(url_for('stable_attendance'))

# run the application
if __name__ == "__main__":
    app.run(host='flask-app', port=5000, debug=True)

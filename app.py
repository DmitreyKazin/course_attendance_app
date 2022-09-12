#!/usr/bin/env python3

# external libraries import
from flask import Flask, render_template, request, redirect, url_for, flash
import secrets

# internal models import
import db

TEMPALTES_FOLDER = './templates'

app = Flask(__name__, template_folder=TEMPALTES_FOLDER)
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key


@app.before_first_request
def create_table():
    db.create_temp_attendance()
    db.create_stable_attendance()


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.route('/')
def stable_attendance():
    students = db.query_all_stable_attendance()
    return render_template('stable.html', students=students)


@app.route('/temp')
def temp_attendance():
    students = db.query_all_temp_attendance()
    return render_template('temp.html', students=students)


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


if __name__ == "__main__":
    app.run(host='flask-app', port=5000, debug=True)

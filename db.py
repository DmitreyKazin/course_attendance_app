#!/usr/bin/env python3

# external libraries import
import mysql.connector
import pandas as pd

# internal modules import
import attendance 

#.env variable package
import os 
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.


MEETINGS_CSV_FOLDER = './csv_files'
MEETINGS_SUB_CSV = './csv_files/all_meetings_submission.csv'

db_connection = mysql.connector.connect(
			        host='mysql',
				port="3306",
			        user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASS'),
			        database=os.getenv('DB_NAME')
		        )

cursor = db_connection.cursor()


def create_temp_attendance():
    cursor.execute(''' DROP TABLE IF EXISTS temp_attendance ''')
    cursor.execute(''' CREATE TABLE temp_attendance (
                        Name VARCHAR(100) NOT NULL,
                        Total_Min VARCHAR(100),
                        Total_Percentage VARCHAR(7))
                 ''')

    attendance.data_eng(MEETINGS_CSV_FOLDER)
   
    df = pd.read_csv(MEETINGS_SUB_CSV, index_col=0)

    for i,row in df.iterrows():
        query = '''INSERT INTO temp_attendance VALUES
	            (%s, %s, %s)'''
        cursor.execute(query, tuple(row))
    db_connection.commit()
    

def query_all_temp_attendance():
    cursor.execute("SELECT * FROM temp_attendance")
    return cursor.fetchall()


def create_stable_attendance():
    cursor.execute(''' CREATE TABLE IF NOT EXISTS stable_attendance (
                        Name VARCHAR(100) NOT NULL PRIMARY KEY,
                        Total_Min VARCHAR(100),
                        Total_Percentage VARCHAR(7))
                 ''')
    db_connection.commit()
   

def query_all_stable_attendance():
    cursor.execute("SELECT * FROM stable_attendance")
    return cursor.fetchall()


def insert_into_stable_attendance(name, total_min, total_percentage):
    record = (name, total_min, total_percentage)
    cursor.execute('''INSERT INTO stable_attendance VALUES
                    (%s, %s, %s)''', record)
    db_connection.commit()


def query_stable_student(name):
    cursor.execute('''
                   SELECT * FROM stable_attendance
                   WHERE name = %s
                   ''', (name,))
    return cursor.fetchone()


def delete_stable_student(name):
    cursor.execute('''
                   DELETE FROM stable_attendance 
                   WHERE name = %s
                   ''', (name,))
    db_connection.commit()


def edit_stable_student(old_name, new_name, total_min, total_percentage):
    cursor.execute('''
                   UPDATE stable_attendance
                   SET name = %s, total_min = %s, total_percentage = %s
                   WHERE name = %s
                   ''', (new_name, total_min, total_percentage, old_name))
    db_connection.commit()


import os

from flask import Flask, render_template, request, send_from_directory, url_for
import mysql.connector
from mysql.connector import Error
import pandas as pd

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            user=user_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

# create and configure the app
app = Flask(__name__, instance_relative_config=True)

@app.route('/Report')
def display_1():
    from_db = []
    pw = '12345678'
    q1 = 'SELECT * FROM test1'
    connection = create_db_connection("localhost", "root", pw, "test1")
    results = read_query(connection, q1)
    for n,v in results:
        from_db.append(v)
    print(from_db)
    
    return render_template('chartjs.html', data = from_db)
    
# a simple page that says hello
@app.route('/hello/')
def hello():
    return 'Hello, World!'
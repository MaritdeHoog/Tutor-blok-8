from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def connect():
    """ Connect to the database.
    :return connection: object - connection to the database
    :return cursor: object - cursor to write queries
    """
    # Establish a connection.

    connection = mysql.connector.connect(
        host="mysql.dehoogjes.nl",
        user="dehoogjesnl",
        db="dehoogjesnl",
        password="HoogKlooster19",
        auth_plugin="mysql_native_password")

    # Open a cursor.
    cursor = connection.cursor()

    # Return the connection and cursor.
    return connection, cursor


def disconnect(connection, cursor):
    """ Disconnect from the database.
    :param connection: object - connection to the database
    :param cursor: object - cursor to write queries
    """
    # Close the cursor and disconnect from the database.
    cursor.close()
    connection.close()


@app.route("/")
def home_page():
    """ Contains the functions around the homepage.
    :return: render of home.html
    """
    return render_template("home.html")


@app.route("/read_excel.html")
def read_excel_page():
    """"
    :return: render of read_excel.html
    """
    return render_template("read_excel.html")


@app.route("/results.html")
def results_page():
    """
    :return: render of results.html
    """
    return render_template("results.html")


@app.route("/database.html")
def database_page():
    """
    :return: render of database.html
    """
    return render_template("database.html")


if __name__ == "__main__":
    app.run()

import jinja2.exceptions
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def connect():
    """ Connect to the database.
    :return connection: object - connection to the database
    :return cursor: object - cursor to write queries
    """
    # Establish a connection.

    mydb = mysql.connector.connect(
        host="mysql.dehoogjes.nl",
        user="dehoogjesnl",
        db="dehoogjesnl",
        password="**************",
        auth_plugin="mysql_native_password")

    # Open a cursor.
    cursor = mydb.cursor()

    # Return the connection and cursor.
    return mydb, cursor


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
# def database_page():
#     """
#     :return: render of database.html
#     """
#     return render_template("database.html")
def database():
    """Database pagina met connectie aan de database
    :return: HTML pagina met resultaten uit de database
    """
    try:
        lijst = []
        # Connectie met de database
        mydb = mysql.connector.connect(
            host="mysql.dehoogjes.nl",
            user="dehoogjesnl",
            db="dehoogjesnl",
            password="**************",
            auth_plugin="mysql_native_password")

        # Open a cursor.
        cursor = mydb.cursor()
        # deze regel kon niet in pep8 want dan doet de query het niet meer
        cursor.execute("select p.patient_id, m.naam, vziekte, z.z_score, t.hoeveelehid from voorspelde_ziektes inner join (select voorspelde_ziektes_vziekte_id, hoeveelehid, methaboliten_met_id from Table_9) t on voorspelde_ziektes.vziekte_id = t.voorspelde_ziektes_vziekte_id inner join (select met_id, naam from metabolieten) m on t.methaboliten_met_id = m.met_id inner join (select z_score, metabolieten_met_id, Personen_persoon_id from z) z on m.met_id = z.metabolieten_met_id inner join (select persoon_id, patient_id from Personen) p on z.Personen_persoon_id = p.persoon_id where p.patient_id = 'P1002.1_Zscore' order by z_score desc limit 10;")
        # inner join Personen P on z.Personen_persoon_id = P.persoon_id
        # Alle resultaten eruit halen

        resultaat = cursor.fetchall()

        # Cursor en database closen
        cursor.close()
        mydb.close()

            # Returnen HTML pagina en resultaat
        return render_template("database.html",
                               len=len(resultaat), invoer=resultaat)
    except SyntaxError:
        print("Er klopt iets niet in de code")
    except TypeError:
        print("Object type klopt niet")
    except NameError:
        print("Kan variabele niet vinden")
    except mysql.connector.errors.ProgrammingError:
        print("Dit bestaat niet in de database")
    except jinja2.exceptions.TemplateNotFound:
        print("Er klopt iets niet bij het aanroepen van de"
              " HTML template")


if __name__ == "__main__":
    app.run()
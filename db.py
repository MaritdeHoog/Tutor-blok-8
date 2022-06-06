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

    connection = mysql.connector.connect(
        host="mysql.dehoogjes.nl",
        user="dehoogjesnl",
        db="dehoogjesnl",
        password="*************",
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
        # Connectie met de database
        connection = mysql.connector.connect(
            host="mysql.dehoogjes.nl",
            user="dehoogjesnl",
            db="dehoogjesnl",
            password="***************",
            auth_plugin="mysql_native_password")

        # Open a cursor.
        cursor = connection.cursor()
        # Dingen invoeren en knopje aan de database linken
        filter = request.args.get("filter", "")
        invoer = request.args.get("invoer", "")
        if filter == "vziekte":
            # deze regel kon niet in pep8 want dan doet de query het niet meer
            cursor.execute("select p.patient_id, m.naam, vziekte, z.z_score, t.hoeveelehid from voorspelde_ziektes inner join (select voorspelde_ziektes_vziekte_id, hoeveelehid, methaboliten_met_id from Table_9) t on voorspelde_ziektes.vziekte_id = t.voorspelde_ziektes_vziekte_id inner join (select met_id, naam from metabolieten) m on t.methaboliten_met_id = m.met_id inner join (select z_score, metabolieten_met_id, Personen_persoon_id from z) z on m.met_id = z.metabolieten_met_id inner join (select persoon_id, patient_id from Personen) p on z.Personen_persoon_id = p.persoon_id where voorspelde_ziektes.vziekte like '%"+invoer+"%' order by hoeveelehid desc limit 20;")
            resultaat = cursor.fetchall()
        else:
            # deze regel kon niet in pep8 want dan doet de query het niet meer
            cursor.execute("select p.patient_id, m.naam, vziekte, z.z_score, t.hoeveelehid from voorspelde_ziektes inner join (select voorspelde_ziektes_vziekte_id, hoeveelehid, methaboliten_met_id from Table_9) t on voorspelde_ziektes.vziekte_id = t.voorspelde_ziektes_vziekte_id inner join (select met_id, naam from metabolieten) m on t.methaboliten_met_id = m.met_id inner join (select z_score, metabolieten_met_id, Personen_persoon_id from z) z on m.met_id = z.metabolieten_met_id inner join (select persoon_id, patient_id from Personen) p on z.Personen_persoon_id = p.persoon_id where p.patient_id like '%"+invoer+"%' order by hoeveelehid desc limit 20;")
            resultaat = cursor.fetchall()
        # inner join Personen P on z.Personen_persoon_id = P.persoon_id
        # Alle resultaten eruit halen


        # Cursor en database closen
        cursor.close()
        connection.close()

            # Returnen HTML pagina en resultaat
        return render_template("database.html",
                               len=len(resultaat), invoer=resultaat)
    except SyntaxError:
        print("Er klopt iets niet in de code")
        return render_template("database.html",
                               len=len(resultaat), invoer=resultaat)
    except TypeError:
        print("Object type klopt niet")
        return render_template("database.html",
                               len=len(resultaat), invoer=resultaat)
    except NameError:
        print("Kan variabele niet vinden")
        return render_template("database.html",
                               len=len(resultaat), invoer=resultaat)
    except mysql.connector.errors.ProgrammingError:
        print("Dit bestaat niet in de database")
        return render_template("database.html",
                               len=len(resultaat), invoer=resultaat)
    except jinja2.exceptions.TemplateNotFound:
        print("Er klopt iets niet bij het aanroepen van de"
              " HTML template")
        return render_template("database.html",
                               len=len(resultaat), invoer=resultaat)


if __name__ == "__main__":
    app.run()

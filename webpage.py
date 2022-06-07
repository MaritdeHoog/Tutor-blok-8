from flask import Flask, render_template, request
import mysql.connector
import plotly.express as px
import pandas as pd
import json
import plotly
from werkzeug.utils import secure_filename
import jinja2
import file_from_webpage


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
        password="**************",
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
    """" handles the process of reading a new Excel-file
    :return: render of read_excel.html
    """
    return render_template("read_excel.html")


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    """ Saves the uploaded file
    :return: render of uploader.html
    """
    # retrieves filename and saves the file
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        print(f.filename)
        new_filename = f.filename.replace(" ", "_")
        # check to see if the file is an excel file
        if "xlsx" not in new_filename:
            pass
        else:
            file_from_webpage.new_data(new_filename)

        return render_template("uploader.html", filename=f.filename)


@app.route("/results.html", methods=['GET', 'POST'])
def results_page():
    """ Based on user selected patient, shows a sunburst plot to
        visualise the metabolic data
    :return: render of results.html
    """
    # retrieves connection with database
    connection, cursor = connect()

    # fetches a list of all patients in the database
    insert = "select patient_id from Personen"
    cursor.execute(insert)
    p_list = [i[0] for i in cursor.fetchall()]

    # returns selection of patient from page
    select = request.form.get('comp_select')

    # default patient name
    if select is None:
        patient_name = "P1002.1_Zscore"
        print(patient_name)
    # patient name from user selection
    else:
        patient_name = str(select)
        print(patient_name)

    # MySQL query to retrieve information from joined tables
    insert = "select patient_id, vziekte, hoeveelehid, naam, z_score " \
             "from Personen " \
             "inner join (select Personen_persoon_id, z_score, metabolieten_met_id " \
             "from z " \
             "where Personen_persoon_id = (select persoon_id " \
             "from Personen " \
             "where patient_id = %(patient)s) " \
             "order by z_score desc " \
             "limit 20) z on persoon_id = z.Personen_persoon_id " \
             "inner join (select naam, met_id " \
             "from metabolieten) m on z.metabolieten_met_id = m.met_id " \
             "inner join (select methaboliten_met_id, hoeveelehid, voorspelde_ziektes_vziekte_id " \
             "from Table_9) t on m.met_id = t.methaboliten_met_id " \
             "inner join (select vziekte, vziekte_id " \
             "from voorspelde_ziektes) v on t.voorspelde_ziektes_vziekte_id = v.vziekte_id"

    # turns retrieved data from MySQL into a pandas dataframe
    data = pd.read_sql(insert, connection, params={'patient': patient_name})
    # makes a new column with name and z-score together
    data['naam_z'] = data['naam'] + " (z = " + data['z_score'].astype(str) + ")"

    # generates the sunburst plot
    fig = px.sunburst(data, path=['patient_id', 'naam_z', 'vziekte'], values="hoeveelehid", width=750, height=750)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("results.html", patients=p_list, graphJSON=graphJSON)


@app.route("/database.html", methods=['GET', 'POST'])
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
            password="**************",
            auth_plugin="mysql_native_password")

        # Open a cursor.
        cursor = connection.cursor()
        # Dingen invoeren en knopje aan de database linken
        filter = request.args.get("filter", "")
        invoer = request.args.get("invoer", "")
        if filter == "vziekte":
            # deze regel kon niet in pep8 want dan doet de query het niet meer
            cursor.execute("select p.patient_id, m.naam, vziekte, z.z_score, t.hoeveelehid from voorspelde_ziektes inner join (select voorspelde_ziektes_vziekte_id, hoeveelehid, methaboliten_met_id from Table_9) t on voorspelde_ziektes.vziekte_id = t.voorspelde_ziektes_vziekte_id inner join (select met_id, naam from metabolieten) m on t.methaboliten_met_id = m.met_id inner join (select z_score, metabolieten_met_id, Personen_persoon_id from z) z on m.met_id = z.metabolieten_met_id inner join (select persoon_id, patient_id from Personen) p on z.Personen_persoon_id = p.persoon_id where voorspelde_ziektes.vziekte like '%"+invoer+"%' order by hoeveelehid desc limit 100;")
            resultaat = cursor.fetchall()
        else:
            # deze regel kon niet in pep8 want dan doet de query het niet meer
            cursor.execute("select p.patient_id, m.naam, vziekte, z.z_score, t.hoeveelehid from voorspelde_ziektes inner join (select voorspelde_ziektes_vziekte_id, hoeveelehid, methaboliten_met_id from Table_9) t on voorspelde_ziektes.vziekte_id = t.voorspelde_ziektes_vziekte_id inner join (select met_id, naam from metabolieten) m on t.methaboliten_met_id = m.met_id inner join (select z_score, metabolieten_met_id, Personen_persoon_id from z) z on m.met_id = z.metabolieten_met_id inner join (select persoon_id, patient_id from Personen) p on z.Personen_persoon_id = p.persoon_id where p.patient_id like '%"+invoer+"%' order by hoeveelehid desc limit 100;")
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

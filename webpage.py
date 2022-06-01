from flask import Flask, render_template, request, redirect
import mysql.connector
import plotly.express as px
import pandas as pd
import json
import plotly


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


@app.route("/results.html", methods=['GET', 'POST'])
def results_page():
    """
    :return: render of results.html
    """
    connection, cursor = connect()

    insert = "select patient_id from Personen"
    cursor.execute(insert)
    p_list = [i[0] for i in cursor.fetchall()]

    select = request.form.get('comp_select')

    if select is None:
        patient_name = "P1002.1_Zscore"
        print(patient_name)
    else:
        patient_name = str(select)
        print(patient_name)

    insert = "select patient_id, vziekte, hoeveelehid, naam, z_score " \
             "from Personen " \
             "inner join (select Personen_persoon_id, z_score, metabolieten_met_id " \
             "from z " \
             "where Personen_persoon_id = (select persoon_id " \
             "from Personen " \
             "where patient_id = %(patient)s) " \
             "order by z_score desc " \
             "limit 15) z on persoon_id = z.Personen_persoon_id " \
             "inner join (select naam, met_id " \
             "from metabolieten) m on z.metabolieten_met_id = m.met_id " \
             "inner join (select methaboliten_met_id, hoeveelehid, voorspelde_ziektes_vziekte_id " \
             "from Table_9) t on m.met_id = t.methaboliten_met_id " \
             "inner join (select vziekte, vziekte_id " \
             "from voorspelde_ziektes) v on t.voorspelde_ziektes_vziekte_id = v.vziekte_id"
    data = pd.read_sql(insert, connection, params={'patient': patient_name})
    data['naam_z'] = data['naam'] + " (z = " + data['z_score'].astype(str) + ")"

    fig = px.sunburst(data, path=['patient_id', 'naam_z', 'vziekte'], values="hoeveelehid", width= 750, height=750)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("results.html", patients=p_list, graphJSON=graphJSON)


# @app.route("/test", methods=['GET', 'POST'])
# def test():
#     select = request.form.get('comp_select')
#
#     connection, cursor = connect()
#     patient_name = str(select)
#     print(patient_name)
#
#     insert = "select patient_id, vziekte, hoeveelehid, naam, z_score " \
#              "from Personen " \
#              "inner join (select Personen_persoon_id, z_score, metabolieten_met_id " \
#              "from z " \
#              "where Personen_persoon_id = (select persoon_id " \
#              "from Personen " \
#              "where patient_id = %(patient)s) " \
#              "order by z_score desc " \
#              "limit 15) z on persoon_id = z.Personen_persoon_id " \
#              "inner join (select naam, met_id " \
#              "from metabolieten) m on z.metabolieten_met_id = m.met_id " \
#              "inner join (select methaboliten_met_id, hoeveelehid, voorspelde_ziektes_vziekte_id " \
#              "from Table_9) t on m.met_id = t.methaboliten_met_id " \
#              "inner join (select vziekte, vziekte_id " \
#              "from voorspelde_ziektes) v on t.voorspelde_ziektes_vziekte_id = v.vziekte_id"
#     data = pd.read_sql(insert, connection, params={'patient': patient_name})
#     data['naam_z'] = data['naam'] + " (z = " + data['z_score'].astype(str) + ")"
#
#     fig = px.sunburst(data, path=['patient_id', 'naam_z', 'vziekte'], values="hoeveelehid")
#     fig.show()
#     return redirect("/results.html", code=302)

# def mp(patient='P1002.1'):
#     connection, cursor = connect()
#     patient_name = patient
#     print(patient_name)
#
#     insert = "select patient_id, vziekte, hoeveelehid, naam, z_score " \
#              "from Personen " \
#              "inner join (select Personen_persoon_id, z_score, metabolieten_met_id " \
#              "from z " \
#              "where Personen_persoon_id = (select persoon_id " \
#              "from Personen " \
#              "where patient_id = '%s') " \
#              "order by z_score desc " \
#              "limit 15) z on persoon_id = z.Personen_persoon_id " \
#              "inner join (select naam, met_id " \
#              "from metabolieten) m on z.metabolieten_met_id = m.met_id " \
#              "inner join (select methaboliten_met_id, hoeveelehid, voorspelde_ziektes_vziekte_id " \
#              "from Table_9) t on m.met_id = t.methaboliten_met_id " \
#              "inner join (select vziekte, vziekte_id " \
#              "from voorspelde_ziektes) v on t.voorspelde_ziektes_vziekte_id = v.vziekte_id"
#     data = pd.read_sql(insert, connection, params=(patient_name,))
#     data['naam_z'] = data['naam'] + " (z = " + data['z_score'].astype(str) + ")"
#
#     fig = px.sunburst(data, path=['patient_id', 'naam_z', 'vziekte'], values="hoeveelehid")
#
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#
#     return graphJSON


@app.route("/database.html")
def database_page():
    """
    :return: render of database.html
    """
    return render_template("database.html")


if __name__ == "__main__":
    app.run()

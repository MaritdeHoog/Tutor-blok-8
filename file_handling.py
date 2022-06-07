import pandas as pd
import re
import mysql.connector


connection = mysql.connector.connect(host="mysql.dehoogjes.nl",
                                     user="dehoogjesnl",
                                     db="dehoogjesnl",
                                     password="**************",
                                     auth_plugin="mysql_native_password")

cursor = connection.cursor()


def read_file(input_file):
    """ Turning excel file into a tsv, retrieving the wanted data
    ":return: mb_list: list containing all necessary data from the file
    """
    mb_list = []
    count = 0

    # import excel file and turns it into a tab separated file
    xlsx_file = pd.read_excel(input_file, index_col=None)
    df = xlsx_file.replace('\n', ' ', regex=True)
    df.to_csv('output_metabolomics.csv', sep='\t', encoding='utf-8', index=False, line_terminator='\n')

    # opens new tsv file
    with open("output_metabolomics.csv") as file:
        for line in file:
            temp = line.split("\t")
            if count == 0:
                temp_list = []
                # saves the important columns
                for i in range(len(temp)):
                    if temp[i] == "name":
                        temp_list.append(i)
                    elif temp[i] == "descr":
                        temp_list.append(i)
                    elif temp[i] == "fluids":
                        temp_list.append(i)
                    elif temp[i] == "tissue":
                        temp_list.append(i)
                    elif temp[i] == "disease":
                        temp_list.append(i)
                    elif temp[i] == "pathway":
                        temp_list.append(i)
                    elif temp[i] == "HMDB_code":
                        temp_list.append(i)
                    # regex query to retrieve all patient codes
                    elif re.match(r"(^P.*_Zscore$)", temp[i]):
                        temp_list.append(i)
                count += 1
            column_list = []
            # adds all data to the corresponding columns
            for i in temp_list:
                column_list.append(temp[i])
            mb_list.append(column_list)
            count += 1

    return mb_list


def fill_ziektes(mb_list):
    """ Fills the "Ziektes" table in the database
    :param mb_list: list with necessary data
    """
    # for all unique values
    unique_list = []

    # MySQL insert query
    insert = "insert into Ziektes(ziekte) values(%s);"

    # loop through the column containing data for this table
    for list in mb_list[1:]:
        temp = list[4].replace("; ", "", 1)
        if temp not in unique_list:
            if temp != "":
                # saves only unique values
                unique_list.append(temp)

    # loops through all the unique values to add to the database
    for i in unique_list:
        # makes a tuple containg the values
        values = (i, )
        # executes the insert combined with values to fill the database
        cursor.execute(insert, values)
        connection.commit()


def fill_pathways(mb_list):
    """ Fills the "pathways" table in the database
    :param mb_list: list with necessary data
    """
    unique_list = []
    insert = "insert into pathways(pathway) values(%s);"

    for list in mb_list[1:]:
        if not re.match(r"(;{1} *$)", list[5]):
            # removes first ";" character
            temp = list[5].replace("; ", "", 1).strip()
            if temp not in unique_list:
                if temp != "":
                    unique_list.append(temp)

    for i in unique_list:
        values = (i, )
        cursor.execute(insert, values)
        connection.commit()


def fill_fluids(mb_list):
    """ Fills the "fluids" table in the database
    :param mb_list: list with necessary data
    """
    unique_list = []
    insert = "insert into fluids(fluid) values(%s);"

    # split fluids per line into unique values
    for list in mb_list[1:]:
        temp = list[2].replace("; ", "", 1).strip()
        if temp not in unique_list:
            if temp != "":
                unique_list.append(temp)

    for i in unique_list:
        values = (i, )
        cursor.execute(insert, values)
        connection.commit()


def fill_metabolieten(mb_list):
    """ Fills the "metabolieten" table in the database
    :param mb_list: list with necessary data
    """
    unique_list = []
    insert = "insert ignore into metabolieten(naam, description, HMDB_code, ziektes_ziekte_id) values(%s, %s, %s, " \
             "(select ziekte_id from Ziektes where ziekte like concat(%s)));"

    for list in mb_list[1:]:
        temp = list[4].replace("; ", "", 1).strip()
        if list[0] not in unique_list:
            if list[0] != "":
                list = [list[0], list[1], list[6], temp]
                unique_list.append(list)

    for i in unique_list:
        values = (i[0], i[1], i[2], i[3])
        cursor.execute(insert, values)
        connection.commit()



def fill_personen(mb_list):
    """ Fills the "Personen" table in the database
    :param mb_list: list with necessary data
    """
    insert = "insert into Personen(patient_id) values(%s);"

    for i in range(len(mb_list[0])):
        if re.match(r"(^P.*_Zscore$)", mb_list[0][i]):
            values = (mb_list[0][i], )
            cursor.execute(insert, values)
            connection.commit()


def fill_z(mb_list):
    """ Fills the "z" table in the database
    :param mb_list: list with necessary data
    """
    insert = "insert ignore into z(z_score, metabolieten_met_id, Personen_persoon_id) values(%s, " \
             "(select met_id from metabolieten where naam like concat(%s)), " \
             "(select persoon_id from Personen where patient_id like concat(%s)));"

    for i in range(len(mb_list[0])):
        if re.match(r"(^P.*_Zscore$)", mb_list[0][i]):
            for list in mb_list[1:]:
                if float(list[i]) > 2 or float(list[i]) < -1.5:
                    values = (list[i], list[0], mb_list[0][i].strip())
                    cursor.execute(insert, values)
                    connection.commit()


if __name__ == "__main__":
    # filename
    mb_file = "Output untargeted metabolomics.xlsx"

    # calls function to create mb_list from the input file
    mb_list = read_file(mb_file)

    # calls all functions to fill the database in order
    # fill_ziektes(mb_list)
    # fill_pathways(mb_list)
    # fill_fluids(mb_list)
    # fill_metabolieten(mb_list)
    # fill_personen(mb_list)
    # fill_z(mb_list)

    # closes connection
    connection.close()

import pandas as pd
import re
import mysql.connector


connection = mysql.connector.connect(host="mysql.dehoogjes.nl",
                                     user="dehoogjesnl",
                                     db="dehoogjesnl",
                                     password="HoogKlooster19",
                                     auth_plugin="mysql_native_password")

cursor = connection.cursor()


def read_file(input_file):
    mb_list = []
    count = 0

    xlsx_file = pd.read_excel(input_file, index_col=None)
    df = xlsx_file.replace('\n', ' ', regex=True)
    df.to_csv('output_metabolomics.csv', sep='\t', encoding='utf-8', index=False, line_terminator='\n')

    with open("output_metabolomics.csv") as file:
        for line in file:
            temp = line.split("\t")
            if count == 0:
                temp_list = []
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
                    elif re.match(r"(^P.*_Zscore$)", temp[i]):
                        temp_list.append(i)
                count += 1
            column_list = []
            for i in temp_list:
                column_list.append(temp[i])
            mb_list.append(column_list)
            count += 1

    return mb_list


def fill_ziektes(mb_list):
    unique_list = []
    # split diseases per line into unique values
    # meer op meer relatie?
    for list in mb_list[1:]:
        if list[4] != "":
            temp = list[4].replace("; ", "", 1)
            temp = temp.replace("'", "")
            if temp not in unique_list:
                unique_list.append(temp)

    for i in unique_list:
        cursor.execute("insert into ziektes(ziekte) values('" + i + "')")
        connection.commit()


def fill_pathways(mb_list):
    unique_list = []
    for list in mb_list[1:]:
        if not re.match(r"(;{1} *$)", list[5]):
            temp = list[5].replace("; ", "", 1)
            if temp not in unique_list:
                unique_list.append(temp)

    for i in unique_list:
        cursor.execute("insert into pathways(pathway) values('" + i + "')")
        connection.commit()


def fill_fluids(mb_list):
    unique_list = []
    # split fluids per line into unique values
    for list in mb_list[1:]:
        temp = list[2].split("; ")[1:]
        for i in temp:
            if i not in unique_list:
                unique_list.append(i)

    for i in unique_list:
        cursor.execute("insert into fluids(fluid) values('" + i + "')")
        connection.commit()


def fill_metabolieten(mb_list):
    for list in mb_list[1:]:
        temp = list[4].replace("; ", "", 1)
        temp = temp.replace("'", "")
        cursor.execute(
            "insert into methaboliten(naam, descerption, HMDB_code, ziektes_ziekte_id) values('" + list[0].replace("'", "") + "', '" +
            list[1].replace("'", "") + "', '" + list[6].replace("'", "") + "', (select ziekte_id "
                                         "                 from ziektes "
                                         "                 where ziekte like concat('" + temp + "')))")
        connection.commit()


def fill_personen(mb_list):
    for i in range(len(mb_list[0])):
        if re.match(r"(^P.*_Zscore$)", mb_list[0][i]):
            cursor.execute(
                " insert into Personen(patient_id) values('" + mb_list[0][i] + "')")
            connection.commit()


def fill_z(mb_list):
    for i in range(len(mb_list[0])):
        if re.match(r"(^P.*_Zscore$)", mb_list[0][i]):
            for list in mb_list[1:]:
                if float(list[i]) > 2 or float(list[i]) < -1.5:
                    cursor.execute(" insert into z(z_score, methaboliten_met_id, Personen_persoon_id) values('" + list[i] + "', (select met_id "
                                   " from methaboliten "
                                   " where naam like concat('" + list[0].replace("'", "") + "')), (select persoon_id "
                                   " from Personen "
                                   " where patient_id like concat('" + mb_list[0][i].strip() + "')))")
                    connection.commit()


if __name__ == "__main__":
    mb_file = "Output untargeted metabolomics.xlsx"

    mb_list = read_file(mb_file)

    # fill_ziektes(mb_list)
    # fill_pathways(mb_list)
    # fill_fluids(mb_list)
    # fill_metabolieten(mb_list)
    # fill_personen(mb_list)
    fill_z(mb_list)

    connection.close()

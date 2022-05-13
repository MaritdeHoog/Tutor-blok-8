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


def fill_database(mb_list):
    for i in range(len(mb_list[0])):
        for list in mb_list[1:]:
            cursor.execute("insert into ziektes(ziekte) values('" + list[4] + "')")
            connection.commit()
            cursor.execute("insert into pathways(pathway) values('" + list[5] + "')")
            connection.commit()

            cursor.execute("insert into fluids(fluid) values('" + list[2] + "')")
            connection.commit()
            cursor.execute("insert into methaboliten(naam, descerption, HMDB_code, ziektes_ziekte_id) values('" + list[0] + "', '" + list[1] + "', '" + list[6] + "', (select ziekte_id "
                       "                 from ziektes "
                       "                 where ziekte like concat('" + list[4] +"')))")
            connection.commit()

    for i in range(len(mb_list[0])):
        for list in mb_list[1:]:
            if re.match(r"(^P.*_Zscore$)", mb_list[0][i]):
                cursor.execute("insert into personen(z_id, z_score) values('" + mb_list[0][i] + "', '" + list[i] + "')")
                connection.commit()


if __name__ == "__main__":
    mb_file = "Output untargeted metabolomics.xlsx"

    mb_list = read_file(mb_file)
    fill_database(mb_list)

    connection.close()

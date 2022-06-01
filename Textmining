from Bio import Entrez
import requests
import mysql.connector

# Initiating a connection with an external database to extract/import data by using the mysql.connector import
connection = mysql.connector.connect(host="mysql.dehoogjes.nl",
                                     user="dehoogjesnl",
                                     db="dehoogjesnl",
                                     password="HoogKlooster19",
                                     auth_plugin="mysql_native_password")

cursor = connection.cursor(buffered=True)


def fetchid():
    """
    :return: ids, a list of pubmed ID's found by searching for a certain metabolite
    """
    # Searching Pubmed for all metabolites
    handle = Entrez.esearch(db="pubmed", term=i[0])
    record = Entrez.read(handle)
    handle.close()
    ids = (record["IdList"])
    return ids


def fetchinfo(idlist):
    # Uses PubTator to fetch a summary of information of previously found articles,
    # it then writes all of the summary's generated to a file and temporarily saves the file.
    joined_string = ",".join(idlist)
    url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/" \
          "pubtator?pmids={0}&concepts=disease".format(joined_string)
    response = requests.get(url)
    with open("test.txt", "wb") as file:
        file.write(response.content)


def fetchdisease():
    """
    Reads through the by fetchinfo created file by selecting the column that contains the found diseases
    and selecting them and their respective frequency.
    :return: temp, a dictionary with diseases as keys and their respective frequency as values
    """
    disease_list = []
    with open("test.txt") as file:
        for line in file:
            # Eliminating lines that dont contain diseases
            if "|t|" or "|a|" not in line:
                if "\t" in line:
                    # Splitting the file by tabs, selecting the disease index and making sure its not empty
                    split = line.split("\t")[3]
                    if split != "":
                        disease_list.append(split)
    # Creating a dictionary with diseases and frequency and sorting it by frequency
    dict_of_counts = {item: disease_list.count(item) for item in disease_list}
    temp = dict(sorted(dict_of_counts.items(), key=lambda item: item[1], reverse=True))
    return temp


def fill_voorspelde_ziektes(temp, metabolieten):
    # Fills the "voorspelde_ziektes" table
    insert = "insert into voorspelde_ziektes(vziekte) values(%s)"
    for i in temp:
        # Filter for diseases that are only found once for significance
        if temp[i] > 1:
            values = (i,)
            try:
                cursor.execute(insert, values)
                connection.commit()
            except mysql.connector.errors.IntegrityError:
                pass
            fill_table_9(i, metabolieten, temp)


def fill_table_9(ziektes, metabolieten, temp):
    # Fills the "table_9" table
    insert = "insert into Table_9(voorspelde_ziektes_vziekte_id, methaboliten_met_id, hoeveelehid) values(" \
             "(select vziekte_id from voorspelde_ziektes where vziekte like concat(%s)), " \
             "(select met_id from metabolieten where naam like concat(%s)), %s);"
    values = (ziektes, metabolieten, temp[ziektes])
    cursor.execute(insert, values)
    connection.commit()


if __name__ == '__main__':
    Entrez.email = "mt.diekman@gmail.com"
    cursor.execute("SELECT naam FROM metabolieten")
    terms = cursor.fetchall()
    for i in terms:
        ids = fetchid()
        fetchinfo(ids)
        temp = fetchdisease()
        fill_voorspelde_ziektes(temp, i[0])

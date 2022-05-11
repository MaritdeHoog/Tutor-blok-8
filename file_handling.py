import pandas as pd
import re


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

    for row in mb_list:
        print(row)


if __name__ == "__main__":
    mb_file = "Output untargeted metabolomics.xlsx"

    read_file(mb_file)

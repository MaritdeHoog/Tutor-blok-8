import file_handling


def new_data(file):
    """ Short function to call the file_handling functions necessary
        to fill the database with new patient data
    :param file: user selected file from webpage
    """
    # reads new file, returns list with important data
    mb_list = file_handling.read_file(file)
    # adds new patients with their z-scores
    file_handling.fill_personen(mb_list)
    file_handling.fill_z(mb_list)

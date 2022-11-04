import pandas as pd
import os

curdir = os.getcwd()
data_fold = os.path.join(curdir,'..','data')

def import_excel_data():
    """

    :return:
    """
    filename = 'sample_data.xlsx'
    file2read = os.path.join(data_fold,filename)

    # read as pandas df
    # location
    locations = pd.read_excel(open(file2read, 'rb'),
                             sheet_name='locaties',
                             engine='openpyxl',
                             keep_default_na=False)
    locations['x'] = [float(x.split(",")[0]) for x in locations["coordinaten"]]
    locations['y'] = [float(x.split(",")[1]) for x in locations["coordinaten"]]
    locations['z'] = [float(x.split(",")[2]) for x in locations["coordinaten"]]

    # sensor
    sensors = pd.read_excel(open(file2read, 'rb'),
                             sheet_name='sensoren',
                             engine='openpyxl',
                             keep_default_na=False)



    # measurements
    measurements = pd.read_excel(open(file2read, 'rb'),
                             sheet_name='metingen',
                             engine='openpyxl',
                             keep_default_na=False)

    return sensors,measurements,locations
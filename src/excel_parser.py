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


    # sensor
    sensors = pd.read_excel(open(file2read, 'rb'),
                             sheet_name='sensoren',
                             engine='openpyxl',
                             keep_default_na=False)

    sensors['x'] = sensors["coordinaten"][0]
    sensors['y'] = sensors["coordinaten"][1]
    sensors['z'] = sensors["coordinaten"][2]

    # measurements
    measurements = pd.read_excel(open(file2read, 'rb'),
                             sheet_name='metingen',
                             engine='openpyxl',
                             keep_default_na=False)

    return sensors,measurements,locations
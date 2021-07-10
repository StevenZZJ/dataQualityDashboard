import pandas as pd
from dashboard import models

# Functions utiles
def handle_upload_csv(f):
    pass


def load_csv(fileurl=''):
    file = '.' + fileurl
    df = pd.read_csv(file)
    return df


def detect_file_type(filename):
    if filename[-3:] == 'csv':
        filetype = 'csv'
    elif filename[-4:] == 'xlsx' or filename[-3:] == 'xls':
        filetype = 'excel'
    else:
        filetype = 'autre'
    return filetype


def get_analyse(id):
    dict = {'completeinfo':'',
            'conform_rate':'',
            'duplicates_rate':'',
            'no_value_missing':'',
            'outliers':'',
            'redundancy':'',
            'same_data_consistency':''}
    query = models.Analyse_Specific.objects.filter(NomDataset_id=id).order_by('NomMes_id')
    for res in query:
        dict[res.NomMes_id] = res.Resultat
    return dict






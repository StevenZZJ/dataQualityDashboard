# Import all libraries
import pandas as pd
import re
# from .models import *
from dashboard import models


def consistencyFunc(fname):
    """

    :param fname:
    :return:
    """
    query = models.CSV.objects.filter(csv='csvs/' + fname)
    nomdataset = query[0].NomDataset
    # count the number of files uploaded with the same name of the current dataset
    countCSV = models.CSV.objects.filter(NomDataset=nomdataset).count()

    # if there is no previous dataset, then this is the first upload, cannot calculate consistency without comparaison
    if countCSV <= 1:
        consistentValue = -1
    # if len(fname) <= 12:
    #     consistentValue = -1

    else:
        # pattern = re.compile(r'^_[A-Za-z0-9]{7,7}.csv$')
        # # if there is no previous dataset, then this is the first upload, cannot calculate consistency without comparaison
        # if pattern.match(fname[-12:]) is None:
        #     consistentValue = -1
        # if there exists previous dataset(s), continue to calculate consistency
        # else:
        # get the id of the current dataset and its previous dataset
        # data = models.CSV.objects.filter(csv__startswith='csvs/' + fname[0:-12]).order_by('-uploaded_at')[
        #        :2].values('id')
        data = models.CSV.objects.filter(NomDataset=nomdataset).order_by('-uploaded_at')[
                   :2].values('id')

        # get the path of the current dataset
        dfPathNew = 'media/' + \
                    models.CSV.objects.filter(csv__startswith='csvs/' + fname[0:-12]).order_by('-uploaded_at')[
                    :1].values(
                        'csv')[0]['csv']

        # get the header of the current dataset
        dfPre = pd.read_csv(dfPathNew, header=0)
        # get the number of rows and columns of the current dataset
        nbRow, nbCol = dfPre.shape
        # get the total number of values in the current dataset
        # nbElements = dfPre.size

        # get the id of the current dataset and its previous dataset
        df1ID = data[0]['id']
        df2ID = data[1]['id']
        # get the list of corresponding columns in each dataset
        df1Format = list(
            models.Attribute.objects.filter(NomDataset=df1ID).values('NomAttribute', 'Format', 'reference'))
        df2Format = list(
            models.Attribute.objects.filter(NomDataset=df2ID).values('NomAttribute', 'Format', 'reference'))

        consistentValue = 0

        # if the Format and reference of the corresponding NomAttribute all match
        # between the current dataset and its previous dataset
        for i in range(len(df1Format)):
            judge = False
            if df1Format[i]['NomAttribute'] == df2Format[i]['NomAttribute']:
                if df1Format[i]['Format'] == df2Format[i]['Format']:
                    if df1Format[i]['reference'] == df2Format[i]['reference']:
                        judge = True
            # add all values of the current row of the current dataset to the number of consistent values
            if judge:
                consistentValue += nbRow

            # Consistency = consistentValue / nbElements * 100
            # return Consistency

    # return the number of consistent values in the current dataset
    return consistentValue


# function to calculate the consistency in one dataset
def consistencyFunc_backup(fname):
    """

    :param fname:
    :return:
    """
    query = models.CSV.objects.filter(csv='csvs/' + fname)
    nomdataset = query[0].NomDataset
    # count the number of files uploaded with the same name of the current dataset
    countCSV = models.CSV.objects.filter(NomDataset=nomdataset).count()

    # if there is no previous dataset, then this is the first upload, cannot calculate consistency without comparaison
    if countCSV <= 1:
        consistentValue = -1

    # if there exists previous dataset(s), continue to calculate consistency
    if countCSV > 1:

        # get the id of the current dataset and its previous dataset
        data = models.CSV.objects.filter(NomDataset=nomdataset).order_by('-uploaded_at')[:2].values('id')

        # get the path of the current dataset
        dfPathNew = 'media/' + models.CSV.objects.filter(NomDataset=nomdataset).order_by('-uploaded_at')[:1].values(
            'csv')[0]['csv']

        # get the header of the current dataset
        dfPre = pd.read_csv(dfPathNew, header=0)
        # get the number of rows and columns of the current dataset
        nbRow, nbCol = dfPre.shape
        # get the total number of values in the current dataset
        # nbElements = dfPre.size

        # get the id of the current dataset and its previous dataset
        df1ID = data[0]['id']
        df2ID = data[1]['id']
        # get the list of corresponding columns in each dataset
        df1Format = list(
            models.Attribute.objects.filter(NomDataset_id=df1ID).values('NomAttribute', 'Format', 'reference'))
        df2Format = list(
            models.Attribute.objects.filter(NomDataset_id=df2ID).values('NomAttribute', 'Format', 'reference'))

        consistentValue = 0

        # if the Format and reference of the corresponding NomAttribute all match
        # between the current dataset and its previous dataset
        for i in range(len(df1Format)):
            judge = False
            if df1Format[i]['NomAttribute'] == df2Format[i]['NomAttribute']:
                if df1Format[i]['Format'] == df2Format[i]['Format']:
                    if df1Format[i]['reference'] == df2Format[i]['reference']:
                        judge = True
            # add all values of the current row of the current dataset to the number of consistent values
            if judge:
                consistentValue += nbRow

            # Consistency = consistentValue / nbElements * 100
            # return Consistency

    # return the number of consistent values in the current dataset
    return consistentValue

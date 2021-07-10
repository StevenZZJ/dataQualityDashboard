# Import all libraries
import numpy as np
import pandas as pd


# function for calculating the duplicate rate in one dataset
def dupRateFunc(dataframe):
    '''

    :param dataframe:
    :return:
    '''

    # read the csv file
    df = dataframe
    duplicateValue = 0
    totalNum = 0

    for i in df.duplicated(keep=False):
        totalNum += 1
        if i:
            duplicateValue += 1

    return duplicateValue


# the function for getting keys with value in dictionary
def get_keys(d, value):
    return [k for k, v in d.items() if v == value]


# the function for calculating the redundancy for a dataset in format csv
def funcRDN(filePath):
    # get the csv file of dataset
    df = pd.read_csv(filePath)
    # put all column headers in a list "dfHeader"
    dfHeader = df.columns.values.tolist()
    # get the column number of dataset
    totalColNum = len(dfHeader)
    totalDupleColNum = 0

    for i in dfHeader:
        # if the data type of one column is object
        if df[i].dtype == 'object':
            # get the name of this column
            columnHeadName = df[i].head().name.__str__()
            # then set datatype of this column as category
            df[columnHeadName] = df[columnHeadName].astype('category').cat.codes
    # get a matrix of correlation
    matrixCorr = df.corr(method='pearson')
    listOfDupleHead = []
    # convert the correlation matrix to dictionary
    DicOfCorr = matrixCorr.to_dict()

    for i in DicOfCorr:
        for j in DicOfCorr:
            if i != j and DicOfCorr[i][j] >= 0.8 and DicOfCorr[i][j] != "NaN":
                listOfDupleHead.append(get_keys(DicOfCorr[i], DicOfCorr[i][j]))
    # the duplicated column names` list
    listOfDupleHead = list(np.array(listOfDupleHead).flatten())
    totalDupleColNum = listOfDupleHead.__len__()
    listOfDupleHead = np.array(listOfDupleHead).reshape(-1, 2)

    RDN = totalDupleColNum / totalColNum

    return RDN

from .Uniqueness import *
from .Validity import Validity
from .Common_Functions import *
from dashboard.forms import CsvUploadForm
from dashboard import models
from .completeness_class import *
from .outlier import *
from .Consistency import *


def chunks(listin, n):
    return [listin[i:i + n] for i in range(0, len(listin), n)]


def intergrateFunction(filePath, idCor, fileName):
    """
    :param filePath: the filepath of csv
    :param idCor: the correlated id of file
    :param fileName:
    :return:
    """

    # read the file by filePath
    df = pd.read_csv(filePath)

    # get list of column names of optional columns
    list1 = list(models.Attribute.objects.filter(NomDataset_id=idCor).filter(Statut=0).values('NomAttribute'))
    listin = []
    columns = df.columns

    # add all items in list1 to listin
    for item in list1:
        listin.append(item['NomAttribute'])
    # drop all optional columns in dataframe
    for i in range(len(columns)):
        if columns[i] in listin:
            df = df.drop(['{}'.format(columns[i])], axis=1)

    # Dimension Completeness
    # measure no_value_missing
    nbValueMissing = missing_values_dataset(df)
    no_value_missing = round(nbValueMissing / df.size, 2)
    # measure completeInfo
    completeInfo = completeInfoFunc(df)
    # --------------------------------------------------------
    # Dimension Consistency
    # measure same Data Consistency
    consistenValues = consistencyFunc(fileName)

    # --------------------------------------------------------
    # Dimension Uniqueness
    # measure Duplicate Rate
    duplicateValue = dupRateFunc(df)

    dupRate = round(duplicateValue / df.size, 4) * 100
    # measure Redundancy
    redundancy = round(funcRDN(filePath),2)

    # --------------------------------------------------------
    # Dimension Validity
    # measure Conform Rate
    V = Validity()
    list2 = list(models.Attribute.objects.filter(NomDataset_id=idCor).filter(Statut=1).values('Format'))
    listin = []
    for item in list2:
        listin.append(item['Format'])

    dicTypeInput = chunks(listin, 1)
    # calculate the conformtype
    conformType = V.conformColoneType(df=df, dic=dicTypeInput, id=idCor)
    sum = 0
    for i in conformType:
        if i:
            sum += 1
        else:
            continue
    typeConformRate = round(sum * 100 / len(conformType), 2)
    # calculate conformRate
    j = 0
    listRate = []

    for i in df.columns:
        columnSelected = df[i]
        typeSelected = listin[j]
        if typeSelected == 'Text':
            columnSelected.replace('\s+', '', regex=True, inplace=True)
            rate = V.columnFormatConformRate(columnSelected, typeSelected)
            listRate.append(rate)
        j += 1

    conformRate = 0
    if len(listRate) == 0:
        formatConformRate = 100
    else:

        for item in listRate:
            conformRate += item
        formatConformRate = conformRate / len(listRate)

    conformRate = round((formatConformRate + typeConformRate) / 2, 2)
    inconformRate = round(100 - conformRate, 2)

    # --------------------------------------------------------
    # Dimension Correlation
    # Outlier
    # nb_outlier = outlierMesure(df)

    date = '2014-12-01'
    sentTotal = df.size
    conversion = 35000
    conversionEmails = 100

    incompleteValues = nbValueMissing
    completeValues = df.size - incompleteValues

    if consistenValues == -1:
        consistenValues = 0
        consistenRate = 0
        inconsistenRate = 0
        inconsistentValues = 0
    else:

        inconsistentValues = pd.read_csv(filePath).size - consistenValues
        consistenRate = round(consistenValues * 100 / pd.read_csv(filePath).size, 2)
        inconsistenRate = round((pd.read_csv(filePath).size - consistenValues) * 100 / pd.read_csv(filePath).size, 2)

    duplicates = duplicateValue
    uniqueValues = df.size - duplicates

    incorrectValues = round(df.size - (df.size * conformRate / 100), 0)
    validValues = round(df.size * conformRate / 100, 0)

    completeRate = completeValues / df.size
    same_data_consistency = consistenRate

    dict = {'date': date,
            'sentTotal': sentTotal,
            'incompleteValues': incompleteValues,
            'completeValues': completeValues,
            'consistenValues': consistenValues,
            'inconsistentValues': inconsistentValues,
            'duplicates': duplicates,
            'uniqueValues': uniqueValues,
            'incorrectValues': incorrectValues,
            'validValues': validValues,
            'conversion': conversion,
            'conversionEmails': conversionEmails,
            'completeRate': round((completeValues / sentTotal) * 100, 2),
            'consistenRate': consistenRate,
            'inconsistenRate': inconsistenRate,
            'incompleteRate': 100 - int((completeValues / sentTotal) * 100),
            'dupRate': round(dupRate, 2),
            'uniqunessRate': round(100 - dupRate-redundancy, 2),
            'redundancy': redundancy,
            'nb_outlier': 10,
            'novaluemiss': no_value_missing,
            'completeInfo': completeInfo,
            'conformRate': conformRate,
            'inconformRate': inconformRate,
            'same_data_consistency': same_data_consistency
            }

    dict1 = {
        'completeinfo': completeInfo,
        'conform_rate': conformRate,
        'duplicates_rate': dupRate,
        'no_value_missing': no_value_missing,
        'outliers': 10,
        'redundancy': redundancy,
        'same_data_consistency': same_data_consistency,
    }

    # save the result to db.analyse_specific
    dictKeyList = list(dict1.keys())

    infoCSV = models.Analyse_Specific.objects.filter(NomDataset=idCor)
    if infoCSV.exists():
        return dict, dict1
    else:
        for key in dictKeyList:
            analyseSpec = models.Analyse_Specific()
            analyseSpec.Resultat = str(dict1[key])
            analyseSpec.NomMes = models.Mesures.objects.filter(NomMes=key).first()
            analyseSpec.NomDataset = models.CSV.objects.filter(csv=filePath[6:]).first()
            analyseSpec.save()

        return dict, dict1

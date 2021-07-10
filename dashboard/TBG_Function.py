from .Consistency import *
from .Uniqueness import *
from .completeness_class import *
from .outlier import *


# delete

def TBG_Function(filePath):
    """

    :param filePath:
    :return:

    """

    # read the file by filePath
    df = pd.read_csv(filePath)

    # Dimension Consistency
    fname = str(filePath)[11:]
    consistentValues = consistencyFunc(fname)
    if consistentValues == -1:
        consistentValues = 0
        inconsistentValues = 0
        print('First time upload, can not calculate Consistency.')
    else:
        inconsistentValues = df.size - consistentValues

    # Dimension Completeness
    incompleteValues = missing_values_dataset(df)
    completeValues = df.size - incompleteValues

    # Dimension Uniqueness
    duplicates = dupRateFunc(df)
    uniqueValues = df.size - duplicates

    # Dimension Validity
    validValues = 15000
    invalidValues = df.size - validValues

    # Dimension Time-related
    timeRelatedValues = 14000
    notTimeRelatedValues = df.size - timeRelatedValues

    dict = {
        'consistentValues': consistentValues,
        'inconsistentValues': inconsistentValues,
        'completeValues': completeValues,
        'incompleteValues': incompleteValues,
        'uniqueValues': uniqueValues,
        'duplicates': duplicates,
        'validValues': validValues,
        'invalidValues': invalidValues,
        'timeRelatedValues': timeRelatedValues,
        'notTimeRelatedValues': notTimeRelatedValues
    }

    return dict

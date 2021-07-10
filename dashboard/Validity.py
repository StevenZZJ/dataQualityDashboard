import re

from dashboard import models


class Validity:
    def __init__(self):
        self.dictV = {'email': '(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$',
                      'portable': '[\+\d]?(\d{2,3}[-\.\s]??\d{2,3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',
                      'Text': '[^%&\',;=?$\x22]+',
                      'integer': '^[1-9]\d*$',
                      'float': '^(-?\d+)(\.\d+)?$'}

        self.dictT = {'Text': ['object'],
                      'integer': ['int64'],
                      'float': ['float64'],
                      'Boolean': ['bool'],
                      'date': ['datetime64']}

    def extractColumns(df):
        """

        Parameters
        ----------
        df : Pandas.DataFrame
            DataFrame with the columns that need to be checked

        Returns
        -------
        cols : list
            Returns a list containing all the columns names of the given DataFrame.

        """
        cols_index = df.columns
        cols = []
        for i in range(len(cols_index)):
            cols.append(cols_index[i])
        return cols

    def getColumnDescription(self, df_desc, all=False, key=''):
        """


        Parameters
        ----------
        df_desc : Pandas.DataFrame or Pandas.Series
            Result of a Pandas.DataFrame.describe().
        all : Boolean, optional
            A flag variable indicates if the given data is for all the columns of just one. The default is False (One column).
        key : String, optional
            Indicates the value needed. The default is ''.
            possible values ['count','mean','std','min','25%','50%','75%','max']

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        if key == '':
            return df_desc
        elif all:
            return df_desc.loc[key]
        else:
            return df_desc[key]

    def getALLColumnDescription(self, df, column='', key=''):
        """


        Parameters
        ----------
        df : TYPE
            DESCRIPTION.
        column : TYPE, optional
            DESCRIPTION. The default is ''.
        key : TYPE, optional
            DESCRIPTION. The default is ''.

        Returns
        -------
        res : TYPE
            DESCRIPTION.

        """
        desc = df.describe()
        if column == '':
            res = self.getColumnDescription(desc, True, key)
        else:
            res = self.getColumnDescription(df[column], False, key)
        return res

    def columnFormatConformRate(self, colone, dic):
        """


        Parameters
        ----------
        colone : Pandas.Series
            A column of the dataset in form of Pandas.Series.
        dic : String
            Regular expression determine the format of the given column.

        Returns
        -------
        float
            Returns the format conform rate of the given column (already in form of %).

        """

        numValid = 0
        numInvalid = 0
        regex = self.dictV[dic]
        pattern = re.compile(regex)
        for i in range(len(colone)):
            if pattern.search(str(colone[i])) is None:
                numInvalid += 1
            else:
                numValid += 1
        return round(numValid * 100 / (numValid + numInvalid), 2)

    def conformColoneType(self, df, dic, id):
        """

        Parameters
        ----------
        colone : Pandas.DataFrame
            DataFrame with the columns that need to be checked
        dic : Array
            List of desired data types

        Returns
        -------
        res : list
            Returns a list containning the desired data types for each column.

        """

        types = []
        res = []
        cols = Validity.extractColumns(df)

        for i in range(len(dic)):
            tp = df[cols[i]].dtype.name
            if dic[i][0] == 'LChoix':
                colname = cols[i]
                query = models.Attribute.objects.filter(NomDataset_id=id).filter(Statut=1).filter(
                    NomAttribute=colname).values('reference')
                ref = query[0]['reference']
                li = ref.split(';')
                s = df[colname]
                flag = True
                for i in s:
                    if i in li:
                        continue
                    else:
                        flag = False
                        break
                res.append(flag)
            else:
                dic[i][0] = self.dictT[dic[i][0]][0]
                for j in range(len(dic[i])):
                    flag = False
                    if tp == dic[i][j]:
                        res.append(True)
                        flag = True
                        break
                    else:
                        continue
                if not flag:
                    res.append(False)
        return res

# 检查数据类型
# 检查数据 conform rate

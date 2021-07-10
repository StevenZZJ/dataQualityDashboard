import numpy as np
import pandas as pd
import unicodedata
from django import forms
from django.forms import modelform_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.template.loader import get_template
from django.urls import reverse

# from web.forms import CsvUploadForm
from dashboard import models
from dashboard.models import CSV, Attribute

pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', 200)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def convert_nan(x):
    if type(x) == str:
        x = ''.join(str(x).split())
        if len(x) == 0:
            x = np.nan
        elif len(x) != 0 and is_number(x):
            x = float(x)
    return x


def coloneData(dataframme):
    df_data = pd.DataFrame()
    for colname, row in dataframme.iteritems():
        list_col = row.values.tolist()
        flag = True
        for i in range(len(list_col)):
            if type(list_col[i]) == str:
                flag = False
        if flag:
            df_col = pd.DataFrame(list_col, columns=[colname])
            df_data[colname] = df_col[colname]
    return df_data


def outlier(dataframme):
    nb_outlier = 0
    outliers = []
    for colname, row in dataframme.iteritems():
        col = row.values.tolist()
        Q1 = np.percentile(col, 25)
        Q3 = np.percentile(col, 75)
        IQR = Q3 - Q1
        ulim = Q3 + 1.5 * IQR
        llim = Q1 - 1.5 * IQR

        for j in range(len(col)):
            if col[j] < llim or col[j] > ulim:
                # print(col[j])
                outliers.append(col[j])
    # nb_outlier  =  number of outlier
    # outlier is a list of nb_outliers
    nb_outlier = len(outliers)
    return nb_outlier


def maxCorr(dataframme, method):
    df_corr = dataframme.corr(method)
    maxCorr = -1
    for colname, row in df_corr.iteritems():
        for i in row:
            if maxCorr < i and i < 1:
                maxCorr = i
                name = colname
                idx = df_corr.loc[df_corr[colname] == i,].index[0]
    # return name, idx, maxCorr
    maxCorr = round(maxCorr, 3)
    return maxCorr


def outlierMesure(dataframe):
    df_pre = dataframe
    df = df_pre.applymap(convert_nan)
    df = df.fillna(df.mean())
    df_data = coloneData(df)
    res = outlier(df_data)
    return res

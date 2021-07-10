import pandas as pd
# from sqlalchemy import false


def missing_values_colonne(filepath, listin):
    df = pd.read_csv(filepath, header=0, sep=',', error_bad_lines=False)
    liste = listin

    print(df)

    columns = df.columns

    for i in range(len(columns)):
        if columns[i] in liste:
            df = df.drop(['{}'.format(columns[i])], axis=1)

    print(df)
    mis_val = df.isnull().sum()
    mis_val_cent = 100 * df.isnull().sum() / len(df)

    tableau_miss = pd.concat([mis_val, mis_val_cent], axis=1)

    # faire le tableau
    mis_val_table_ren_columns = tableau_miss.rename(columns={0: 'NB valeurs manquantes', 1: 'total en %'})
    mis_val_table_ren_columns = mis_val_table_ren_columns[mis_val_table_ren_columns.iloc[:, 1] != 0].sort_values(
        'total en %', ascending=False).round(1)

    return print(mis_val_table_ren_columns)


def missing_values_dataset(dataframe):
    df = dataframe

    nb_total_values_missing = 0

    for i in df.isnull().sum().T:
        # nb_total_values_missing += df.isnull().sum().T[i]
        nb_total_values_missing += i

    # for i in df.isnull().sum().sum():
    #     nb_total_values_missing = i

    return nb_total_values_missing


def completeInfoFunc(dataframe):
    df = dataframe

    kkk = df[df.isnull().T.any()]
    row, columns = kkk.shape
    rowdf, coldf = df.shape
    completeInfo = round(1 - (row / rowdf), 4)

    return completeInfo

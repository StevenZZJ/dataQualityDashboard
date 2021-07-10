import json
import random

from django.utils.safestring import SafeString

# debug

'''
1. Step 1: Put your libraries in the same directory as views.py
2. Step 2: Import your libraries here with a '.'
'''
from .completeness_class import *
from .outlier import *
from .IntegrateFunction import *
from dashboard.forms import CsvUploadForm
from dashboard import models


# Create your views here.
def upload(request):
    '''

    :param request:
    :return: page upload
    '''
    # Handle file upload
    if request.method == 'POST':
        isupdate = False
        form = CsvUploadForm(request.POST, request.FILES)
        # form = CsvUploadForm(request.POST)
        if form.is_valid():
            # if models.Dataset.objects.filter(NomDataset=form.cleaned_data['nomdataset']):
            #     isupdate = True
            # else:

            nomdataset = form.cleaned_data['nomdataset']
            cat = models.Categories.objects.get(id=form.cleaned_data['category'])
            pays = models.Pays.objects.get(id=form.cleaned_data['pays'])
            annee = models.Annee.objects.get(id=form.cleaned_data['annee'])
            sep = form.cleaned_data['sep']
            newdataset = models.CSV(csv=request.FILES['csv'],
                                    NomDataset=nomdataset,
                                    CatDataset=cat,
                                    PaysDataset=pays,
                                    annee=annee,
                                    sep=sep)
            newdataset.save()
            # query = models.CSV.objects.raw("select * from dashboard_csv d where d.uploaded_at in " +
            #                                "(select max(uploaded_at) from dashboard_csv " +
            #                                "where NomDataset='" + nomdataset + "' group by NomDataset)")
            query = models.CSV.objects.filter(NomDataset=nomdataset).order_by('-uploaded_at').first()
            fname = query.csv.name
            fname = fname[5:]
            return HttpResponseRedirect(reverse('choose_type', args=(fname,)))

    else:
        form = CsvUploadForm()  # A empty, unbound form

    # Load documents for the list page
    documents = models.CSV.objects.all()

    # Render the upload page with the documents and the form
    return render(request, 'upload.html', {'documents': documents, 'form': form})


def choixType(request, fname):
    df_pre = pd.read_csv('media/csvs/' + fname)
    csv = 'csvs/' + fname
    nom_dataset = models.CSV.objects.filter(csv=csv).values_list('NomDataset', flat=True).first()
    labels = list(df_pre.columns.values)
    dfsmall = df_pre[:5]

    j = dfsmall.to_json(orient='records')
    return render(request, 'choose_type.html',
                  {'data': SafeString(j), 'fname': fname, 'nom_dataset': nom_dataset, 'labels': labels})


def gettype(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        nom_dataset = request.POST.get('nom_dataset')
        type = request.POST.getlist('type')
        float = request.POST.getlist('float')
        boolean = request.POST.getlist('boolean')
        date = request.POST.getlist('date')
        text = request.POST.getlist('text')
        listechoix = request.POST.getlist('listechoix')
        reference = []
        for i in range(len(float)):
            if float[i] != '':
                reference.append(float[i])
            elif boolean[i] != '':
                reference.append(boolean[i])
            elif date[i] != '':
                reference.append(date[i])
            elif text[i] != '':
                reference.append(text[i])
            elif listechoix[i] != '':
                reference.append(listechoix[i])
            else:
                reference.append('')
    df_pre = pd.read_csv('media/csvs/' + fname)
    labels = list(df_pre.columns.values)
    csv = 'csvs/' + fname
    id_csv = models.CSV.objects.filter(csv=csv).values_list('id', flat=True).first()
    for i in range(len(labels)):
        attrib = models.Attribute()
        attrib.NomAttribute = labels[i]
        attrib.Format = type[i]
        attrib.NomDataset_id = id_csv
        attrib.reference = reference[i]
        statut = request.POST.get("statut_" + labels[i])
        attrib.Statut = statut
        attrib.save()

    consisV = consistencyFunc(fname)
    context = {'fname': fname, 'nom_dataset': nom_dataset, 'labels': labels, 'type': type,
               'listechoix': listechoix, 'float': float, 'date': date, 'boolean': boolean, 'text': text,
               'consisV': consisV}

    return render(request, 'showtype.html', context)


def accueil(request):
    categories = models.Categories.objects.all()
    pays = models.Pays.objects.all()
    datasets = []
    dataset = {'csv': '',
               'date': '',
               'name': '',
               'year': '',
               'sep': '',
               'cat': '',
               'pays': '',
               'score': 0,
               # 'dimensions': ''
               'consistency': 0,
               'completeness': 0,
               'uniqueness': 0,
               'validity': 0,
               'type': ''
               }
    '''
    Raw query:
    select * 
    from dashboard_csv d 
    where d.uploaded_at in (
        select max(uploaded_at) 
        from dashboard_csv 
        group by NomDataset)
    '''
    query = models.CSV.objects.raw(
        'select * from dashboard_csv d where d.uploaded_at in ' +
        '(select max(uploaded_at) from dashboard_csv group by NomDataset)')
    for res in query:
        scores = get_analyse(res.id)
        # notes = [random.randint(80, 100) for i in range(4)]
        notes = [float(scores['same_data_consistency']), float(scores['completeinfo']) * 100,
                 100 - float(scores['duplicates_rate']),
                 float(scores['conform_rate'])]
        filename = res.csv.name
        fname = filename[5:]
        # url = reverse('analyse_individual', args=(fname,))
        filetype = detect_file_type(fname)

        line = [fname,
                res.uploaded_at,
                res.NomDataset,
                res.annee.annee,
                res.sep,
                res.CatDataset.NomCategory,
                res.PaysDataset.NomPays,
                round(sum(notes) / len(notes), 2),
                # json.dumps([random.randint(80, 100) for i in range(4)])
                ] + notes + ['dashboard/img/' + filetype + '.png']
        datasets.append(dict(zip(dataset.keys(), line)))

    context = {'categories': categories,
               'pays': pays,  # may be adding truncating to pays in order to display in two columns
               'datasets': datasets,
               'datasetcount': len(datasets)
               }
    return render(request, 'accueil.html', context)


def analyseIndi(request, fname):
    # If the file name is less than 12, the file is the first upload
    if len(fname) <= 12:
        data = \
            list(models.CSV.objects.filter(csv__startswith='csvs/' + fname).order_by('-uploaded_at')[:1].values('csv'))[
                0][
                'csv']
        filepath = 'media/' + data
        idCor = \
            list(models.CSV.objects.filter(csv__startswith='csvs/' + fname).order_by('-uploaded_at')[:1].values('id'))[
                0][
                'id']

        # calculate all measures by integrateFunction
        # write all measures in dict1
        dict1, dict2 = intergrateFunction(filepath, idCor, fname)

        return render(request, 'statistics.comment.html',
                      {'date': dict1['date'], 'sentTotal': dict1['sentTotal'],
                       'incompleteValues': dict1['incompleteValues'],
                       'completeValues': dict1['completeValues'], 'consistenValues': dict1['consistenValues'],
                       'inconsistentValues': dict1['inconsistentValues'], 'duplicates': dict1['duplicates'],
                       'uniqueValues': dict1['uniqueValues'], 'incorrectValues': dict1['incorrectValues'],
                       'validValues': dict1['validValues'], 'conversion': dict1['conversion'],
                       'conversionEmails': dict1['conversionEmails'], 'completeRate': dict1['completeRate'],
                       'consistenRate': dict1['consistenRate'], 'inconsistenRate': dict1['inconsistenRate'],
                       'incompleteRate': dict1['incompleteRate'], 'dupRate': dict1['dupRate'],
                       'uniqunessRate': dict1['uniqunessRate'], 'redundancy': dict1['redundancy'],
                       'nb_outlier': dict1['nb_outlier'], 'novaluemiss': dict1['novaluemiss'],
                       'completeInfo': dict1['completeInfo'], 'conformRate': dict1['conformRate'],
                       'inconformRate': dict1['inconformRate'], 'same_data_consistency': dict1['same_data_consistency']
                       })

    elif len(fname) > 12:
        data = \
            list(models.CSV.objects.filter(csv__startswith='csvs/' + fname).order_by('-uploaded_at')[:1].values(
                'csv'))[0]['csv']
        filepath = 'media/' + data
        idCor = \
            list(models.CSV.objects.filter(csv__startswith='csvs/' + fname).order_by('-uploaded_at')[:1].values(
                'id'))[0]['id']

        # calculate all measures by integrateFunction
        # write all measures in dict1
        dict1, dict2 = intergrateFunction(filepath, idCor, fname)

        return render(request, 'statistics.comment.html',
                      {'date': dict1['date'], 'sentTotal': dict1['sentTotal'],
                       'incompleteValues': dict1['incompleteValues'],
                       'completeValues': dict1['completeValues'], 'consistenValues': dict1['consistenValues'],
                       'inconsistentValues': dict1['inconsistentValues'], 'duplicates': dict1['duplicates'],
                       'uniqueValues': dict1['uniqueValues'], 'incorrectValues': dict1['incorrectValues'],
                       'validValues': dict1['validValues'], 'conversion': dict1['conversion'],
                       'conversionEmails': dict1['conversionEmails'], 'completeRate': dict1['completeRate'],
                       'consistenRate': dict1['consistenRate'], 'inconsistenRate': dict1['inconsistenRate'],
                       'incompleteRate': dict1['incompleteRate'], 'dupRate': dict1['dupRate'],
                       'uniqunessRate': dict1['uniqunessRate'], 'redundancy': dict1['redundancy'],
                       'nb_outlier': dict1['nb_outlier'], 'novaluemiss': dict1['novaluemiss'],
                       'completeInfo': dict1['completeInfo'], 'conformRate': dict1['conformRate'],
                       'inconformRate': dict1['inconformRate'], 'same_data_consistency': dict1['same_data_consistency']
                       })


# 从upload加载过来 url get 传值
# 先计算前端所需的数值，保存到数据库
# 再将这些数据渲染到前端模板 rapport general
def analyseGeneral(request):
    # Rapport general
    # Analyse par catégorie
    ac = []
    correctValues = 0
    TotalValues = 0
    itemAC = {}
    catList = list(models.Categories.objects.all().values('id', 'NomCategory'))
    for i in range(len(catList)):
        itemAC = {}
        nameList = list(models.CSV.objects.all().filter(CatDataset_id=catList[i]['id']).values('csv'))
        idList = list(models.CSV.objects.all().filter(CatDataset_id=catList[i]['id']).values('id'))
        itemAC['Cat'] = catList[i]['NomCategory']
        correctValues = 0
        TotalValues = 0
        for j in range(len(idList)):
            itemAnalyse = list(models.Analyse_Specific.objects.all().filter(NomDataset_id=idList[j]['id']).values())
            correctValues += pd.read_csv('media/' + nameList[j]['csv']).size * (
                float(itemAnalyse[1]['Resultat'])) * 0.01
            TotalValues += pd.read_csv('media/' + nameList[j]['csv']).size
            itemAC['totalValues'] = int(TotalValues)
            itemAC['correctValues'] = int(correctValues)
        ac.append(itemAC)

    nameList = list(models.CSV.objects.all().values('csv'))
    idList = list(models.CSV.objects.all().values('id'))
    acJson = {'id': ac}

    # Tendances
    yearList = list(models.Annee.objects.all().values('id', 'annee'))
    item = {}
    yearJson = {'id': []}
    for i in range(len(yearList)):
        item = {}
        item['Annee'] = yearList[i]['annee']
        nameList1 = list(models.CSV.objects.all().filter(annee_id=yearList[i]['id']).values('csv'))
        idList1 = list(models.CSV.objects.all().filter(annee_id=yearList[i]['id']).values('id'))
        total = 0
        totalRate = 0
        for j in range(len(idList1)):
            itemAnalyse = list(models.Analyse_Specific.objects.all().filter(NomDataset_id=idList[j]['id']).values())
            total += 1
            totalRate += float(itemAnalyse[1]['Resultat'])
            for q in range(len(idList1)):
                itemAnalyse = list(models.Analyse_Specific.objects.all().filter(NomDataset_id=idList[j]['id']).values())
                item['Lower'] = 0
                if float(itemAnalyse[1]['Resultat']) < totalRate / total:
                    item['Lower'] += 1
        item['Total'] = total
        yearJson['id'].append(item)

    # Erreurs par dimension
    incompleteRate = 0
    dupRate = 0
    inconformRate = 0
    inconsistenRate = 0

    # get a list of all id and filename from database
    list1 = list(models.CSV.objects.all().values('id', 'csv'))
    # count the total number of files uploaded
    numCSV = len(list1)

    # call for intergrateFunction to calculate the percentage of errors per dimension for each dataset
    for i in range(len(list1)):
        dict1 = {}
        dict2 = {}
        idCor = list1[i]['id']
        filename = list1[i]['csv'][5:]
        filepath = 'media/' + list1[i]['csv']
        dict1, dict2 = intergrateFunction(filepath, idCor, filename)
        inconsistenRate += dict1['inconsistenRate']
        incompleteRate += dict1['incompleteRate']
        dupRate += dict1['dupRate']
        inconformRate += dict1['inconformRate']

        # calculate the average incorrecte rate of each dimension of all datasets
        # Cohérence
        averageInconsistentRate = round(inconsistenRate / numCSV, 2)
        # Complétude
        averageIncompleteRate = round(incompleteRate / numCSV, 2)
        # Unicité
        averageDupRate = round(dupRate / numCSV, 2)
        # Validité
        averageInconformRate = round(inconformRate / numCSV, 2)
    # -------------------------------------------------------------------------------------------------

    # Types de fichier en pourcentage
    typeCSV = 0
    for i in range(len(list1)):
        filetype = list1[i]['csv'][:3]
        if filetype == "csv":
            typeCSV = typeCSV + 1
    typePercentage = typeCSV / numCSV * 100

    # -------------------------------------------------------------------------------------------------
    # Les 5 meilleurs datasets
    # call for intergrateFunction to calculate the average score of 4 dimensions for each dataset
    list3 = []
    itemAverage = {}
    for i in range(len(list1)):
        itemAverage = {}
        idCor = list1[i]['id']
        filename = list1[i]['csv'][5:]
        filepath = 'media/' + list1[i]['csv']
        dict1, dict2 = intergrateFunction(filepath, idCor, filename)
        averageScore = round(
            (dict1['completeRate'] + dict1['consistenRate'] + dict1['uniqunessRate'] + dict1['conformRate']) / 4, 2)
        itemAverage = {'filename': filename, 'averageScore': averageScore, 'url': filename}
        list3.append(itemAverage)

    inter = {}
    flag = False
    countFlag = 0

    while not flag:
        countFlag = 0
        for j in range(len(list3) - 1):
            if list3[j]['averageScore'] < list3[j + 1]['averageScore']:
                countFlag += 1
                inter = list3[j]
                list3[j] = list3[j + 1]
                list3[j + 1] = inter

        if countFlag == 0:
            flag = True
            break
    urlOfFile = []
    # Contribution graph
    data = {'id': []}
    for i in range(len(idList)):
        itemAnalyse = list(models.Analyse_Specific.objects.all().filter(NomDataset_id=idList[i]['id']).values())
        ErrCount = pd.read_csv('media/' + nameList[i]['csv']).size * (100 - float(itemAnalyse[1]['Resultat'])) * 0.01
        dupRate = float(itemAnalyse[2]['Resultat'])
        item = {'name': nameList[i]['csv'][5:], 'dupliRate': dupRate,
                'completeness': itemAnalyse[0]['Resultat'], 'url': nameList[i]['csv'][5:],
                'Err': int(ErrCount)}
        data['id'].append(item)
        urlOfFile.append(item['url'])

    datasetJsonString = json.dumps(data)
    acJson = json.dumps(acJson)
    yearJson = json.dumps(yearJson)

    return render(request, 'TBGeneral.html', {'dataSetJson': datasetJsonString, 'acJson': acJson, 'yearJson': yearJson,
                                              'averageInconsistentRate': averageInconsistentRate,
                                              'averageIncompleteRate': averageIncompleteRate,
                                              'averageDupRate': averageDupRate,
                                              'averageInconformRate': averageInconformRate,
                                              'typePercentage': typePercentage,
                                              'list3': list3[0:5],
                                              'urlOfFile': urlOfFile
                                              })

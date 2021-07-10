from django.urls import path

from . import views

urlpatterns = [
    path('analsye_individual/<str:fname>', views.analyseIndi, name='analyse_individual'),
    path('', views.accueil, name='accueil'),
    # path('index', views.index, name='index'),
    path('choose_type/<str:fname>', views.choixType, name='choose_type'),
    path('showtype', views.gettype, name='showtype'),
    path('analyse_general', views.analyseGeneral, name='analyse_general'),
    path('upload', views.upload, name='upload')
]

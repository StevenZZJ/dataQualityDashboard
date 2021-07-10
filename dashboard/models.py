import datetime
from django.db import models


def year_choices():
    return [(r, r) for r in range(1984, datetime.date.today().year + 1)]


# Create your models here.
class Dimentions(models.Model):
    NomDim = models.CharField(max_length=20, primary_key=True)


class Mesures(models.Model):
    NomMes = models.CharField(max_length=50, primary_key=True)
    Unite = models.CharField(max_length=50, null=True)
    NomDim = models.ForeignKey(Dimentions, on_delete=models.CASCADE)


class Categories(models.Model):
    NomCategory = models.CharField(max_length=50)
    Description = models.CharField(max_length=200, null=True)


class Pays(models.Model):
    NomPays = models.CharField(max_length=50)


class Annee(models.Model):
    annee = models.IntegerField()


class CSV(models.Model):
    # description = models.CharField(max_length=355, blank=True)
    csv = models.FileField(upload_to='csvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    NomDataset = models.CharField(max_length=50)
    CatDataset = models.ForeignKey(Categories, on_delete=models.CASCADE)
    PaysDataset = models.ForeignKey(Pays, on_delete=models.CASCADE)
    annee = models.ForeignKey(Annee, on_delete=models.CASCADE)
    sep = models.CharField(max_length=50)

    class Meta:
        unique_together = ("NomDataset", "uploaded_at")


class Attribute(models.Model):
    NomAttribute = models.CharField(max_length=50)
    Format = models.CharField(max_length=50)
    Statut = models.CharField(max_length=50, null=True)
    NomDataset = models.ForeignKey(CSV, on_delete=models.CASCADE)
    reference = models.CharField(max_length=255, null=True)


class Fonction(models.Model):
    NomFonction = models.CharField(max_length=50, primary_key=True)
    Formule = models.CharField(max_length=100)
    Valeurs = models.CharField(max_length=50)
    Resultat = models.CharField(max_length=50, null=True)
    Interpretation = models.CharField(max_length=50, null=True)
    NomMes = models.ForeignKey(Mesures, on_delete=models.CASCADE)


class Analyse_General(models.Model):
    NomMes = models.ForeignKey(Mesures, on_delete=models.CASCADE)
    NomDataset = models.ForeignKey(CSV, on_delete=models.CASCADE)
    Resultat = models.CharField(max_length=50)

    class Meta:
        unique_together = (("NomMes", "NomDataset"),)


class Analyse_Specific(models.Model):
    NomMes = models.ForeignKey(Mesures, on_delete=models.CASCADE)
    NomDataset = models.ForeignKey(CSV, on_delete=models.CASCADE)
    Resultat = models.CharField(max_length=50)

    class Meta:
        unique_together = (("NomMes", "NomDataset"),)


class User(models.Model):
    gender = (('M', 'Male'),
              ('F', 'Female'))
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='Male')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["c_time"]
        verbose_name = 'User'
        verbose_name_plural = 'Users'

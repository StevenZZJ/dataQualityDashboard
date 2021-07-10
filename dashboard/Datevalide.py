import os.path
import datetime
from dateutil.relativedelta import relativedelta

# var find path
import os


class Lastmodif:
    def diftoday(modification, date_jour):

        print(os.path.abspath("text.docx"))

        modification = datetime.date.fromtimestamp(os.path.getmtime("C:\\Users\\DELL\\Desktop\\text.docx"))
        print("Dernière modification: %s" % modification)

        date_jour = datetime.date.today()
        print("Date du jour: %s" % date_jour)

        difference_in_days = relativedelta(date_jour, modification).days
        difference_in_years = relativedelta(date_jour, modification).years

        if (difference_in_years < 1):
            res = difference_in_days
            return res
            # print("Dernière modification: %s jours" % difference_in_days)
        elif (difference_in_years < 5):
            res = (difference_in_years, difference_in_days)
            return res
            # print("Dernière modification: %s annees %s jours" % (difference_in_years, difference_in_days))
        else:
            res = difference_in_years
            return res
            # print("Dernière modification: %s annes. Pensez a actualiser vos donnes" % difference_in_years)
        print(res)

# standard library
import random
import unicodedata
from datetime import datetime, timedelta, date

# django library
from django import template


register = template.Library()

###FILTER###
@register.filter()
def pesel(birthday):
    if isinstance(birthday, date):
        y=str(birthday.year)[2:]
        if len(str(birthday.month)) < 2:
            m = '0' + str(birthday.month)
        else:
            m = str(birthday.month)
        if len(str(birthday.day)) < 2:
            d = '0' + str(birthday.day)
        else:
            d = str(birthday.day)
        l5d = random.randint(5,99999+1)
        return '{}{}{}{}'.format(y,m,d,l5d)


###FILTER###
@register.filter()
def realization(date_of_visit):
    ''' Returns the date after 30 days named dor = date of realization'''
    if isinstance(date_of_visit, date):
        # dor = date of realization of medical prescription
        dor = date_of_visit + timedelta(days=30)
    else:
        date_of_visit = datetime.strptime(date_of_visit, '%Y-%m-%d')
        dor = date_of_visit.date() + timedelta(days=30)

    return dor.__format__('%d.%m.%Y')


###FILTER###
# @register.filter()
# def antibiotic_realization(date_of_visit):
#     ''' Returns the date after 7 days named dor = date of realization'''
#     if isinstance(date_of_visit, date):
#         # dor = date of realization of medical prescription
#         dor = date_of_visit + timedelta(days=7)
#     else:
#         date_of_visit = datetime.strptime(date_of_visit, '%Y-%m-%d')
#         dor = date_of_visit.date() + timedelta(days=7)
#
#     return dor.__format__('%d.%m.%Y')


###FILTER###
# remove polish diacritical signs
@register.filter()
def remdiac(txt):
    return ''.join(c for c in unicodedata.normalize('NFD', txt) if not unicodedata.combining(c))

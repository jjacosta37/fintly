from datetime import datetime, timedelta
import locale
locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')
from dateutil.relativedelta import relativedelta

def return_month(month_name):
    datetime_object = datetime.strptime(month_name, "%B")
    month_number = datetime_object.month
    return month_number

def return_income_date_range(month_name):
    lst = []
    datetime_object = datetime.strptime(month_name +' 2021', "%B %Y")
    lst.append(datetime_object - timedelta(days=21))
    lst.append(datetime_object + timedelta(days=9))
    return lst

def proyect_savings(income, expenses):
    current_day = datetime.now().day
    proyected_expenses = expenses / current_day * 31
    return income - proyected_expenses

def last_twelveMonths_list():
    month_list = [(datetime.now() - relativedelta(months=11) + relativedelta(months=i)).strftime("%Y-%m") for i in range(12)]
    return month_list

    
    
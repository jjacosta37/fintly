import json
import time

from django.db.models import Sum
from django.db.models.functions import TruncMonth
from mixpanel import Mixpanel
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from fintly import belvo_api, settings

from . import python_functions
from .models import Transaction, UserLink

mp = Mixpanel(settings.MIXPANEL_TOKEN)

######### API VIEWS APP #########


@api_view(['GET'])
def montlhy_categories(request):
    current_user = request.user
    categories_month_list = (Transaction.objects
                             .filter(user_id=current_user, type='OUTFLOW')
                             .dates('transaction_date', 'month'))

    def categories_by_month(month):
        category_groupby = (Transaction.objects
                            .filter(transaction_date__month=month.month, transaction_date__year=month.year, user_id=current_user, type='OUTFLOW', isTransaction=False)
                            .values('category')
                            .order_by('category')
                            .annotate(total_price=Sum('amount'))
                            .order_by('-total_price'))
        response = {i['category']: i['total_price'] for i in category_groupby}
        return response

    categories_map = {i.strftime("%Y-%m"): categories_by_month(i)
                      for i in categories_month_list}
    month_list = python_functions.last_twelveMonths_list()
    response = {i: categories_map.get(i) or {} for i in month_list}
    return Response(response)


@api_view(['GET'])
def monthly_expenses(request, month=""):
    current_user = request.user
    month_list = python_functions.last_twelveMonths_list()
    expenses_by_month = (Transaction.objects
                         .filter(user_id=current_user, type='OUTFLOW', isTransaction=False)
                         .annotate(month=TruncMonth('transaction_date'))
                         .values('month').order_by('month')
                         .annotate(expense=Sum('amount')))

    monthly_expenses_map = {i['month'].strftime(
        "%Y-%m"): int(i['expense']) for i in expenses_by_month}

    response = {i: {'expense': monthly_expenses_map.get(
        i) or 0} for i in month_list}

    if (month != ""):
        response = response[month]

    return Response(response)


@api_view(['GET'])
def monthly_incomes(request, month=""):
    current_user = request.user
    month_list = python_functions.last_twelveMonths_list()
    income_by_month = (Transaction.objects
                       .filter(user_id=current_user, type='INFLOW', category='Income & Payments', isTransaction=False)
                       .annotate(month=TruncMonth('transaction_date'))
                       .values('month')
                       .order_by('month')
                       .annotate(income=Sum('amount')))

    monthly_incomes_map = {i['month'].strftime(
        "%Y-%m"): int(i['income']) for i in income_by_month}

    response = {i: {'income': monthly_incomes_map.get(
        i) or 0} for i in month_list}

    if (month != ""):
        response = response[month]

    return Response(response)


@api_view(['GET'])
def get_user_balances(request):
    current_user = request.user
    link_ids = UserLink.objects.filter(user=current_user)
    balances = []
    for user in link_ids:
        balances.append(belvo_api.get_balances(user.link_id))

    return Response(balances)


@api_view(['GET'])
def expenses_list_by_month(request):
    date = request.query_params.get('month')
    date_list = date.split('-')
    requested_category = request.query_params.get('category')
    short_list = request.query_params.get('short_list')
    month_number = date_list[1]
    year_number = date_list[0]
    current_user = request.user

    if short_list == 'True':
        expense_list = (Transaction.objects
                        .filter(user_id=current_user)
                        .values().order_by('-transaction_date')[0:5])

    elif requested_category == "All":
        expense_list = (Transaction.objects
                        .filter(user_id=current_user, transaction_date__month=month_number,
                                transaction_date__year=year_number)
                        .values()
                        .order_by('-transaction_date'))
    else:
        expense_list = (Transaction.objects
                        .filter(user_id=current_user, transaction_date__month=month_number,
                                transaction_date__year=year_number,
                                category__contains=requested_category)
                        .values()
                        .order_by('-amount'))

    return Response(expense_list)


@api_view(['GET'])
def get_expenses_category_list(request):
    date = request.query_params.get('month')
    date_list = date.split('-')
    month_number = date_list[1]
    year_number = date_list[0]
    current_user = request.user
    categories_response = (Transaction.objects
                           .filter(user_id=current_user, transaction_date__month=month_number, transaction_date__year=year_number, isTransaction=False)
                           .values('category')
                           .distinct())
    categories_list = [i['category'] for i in categories_response]

    return Response(categories_list)


@api_view(['PUT'])
def is_transaction(request):
    data = request.data
    transaction = Transaction.objects.get(id=data['id'])
    transaction.isTransaction = data['isTransaction']
    transaction.save()
    return Response(data)


@api_view(['PUT'])
def category(request):
    data = request.data
    transaction = Transaction.objects.get(id=data['id'])
    transaction.category = data['category']
    transaction.save()

    return Response(data)


@api_view(['GET'])
def user_links(request):
    current_user = request.user
    links_list = UserLink.objects.filter(
        user_id=current_user).values('link_id')
    return Response(links_list)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def transactions_historical_update_webhook(request):
    start_time = time.time()
    data = json.loads(request.body)
    webhook_code = data['webhook_code']
    webhook_type = data['webhook_type']
    historical_data = data['data']
    link = data['link_id']

    if (webhook_type == "TRANSACTIONS" and webhook_code in ('historical_update')):
        user_link = UserLink.objects.get(link_id=link)
        transactions = belvo_api.get_transactions(
            link_id=link, days_of_transactions=120)
        belvo_api.addTransactionsToDB(transactions, user_link.user)
        mp.track(user_link.user.username, 'Historical Update Webhook', {
            'Webhook Data': historical_data, 'Get Transactions': len(transactions)
        })
        print("--- Historical Transactions added in %s seconds ---" %
              (time.time() - start_time))

    return Response()


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def new_transactions_webhook(request):
    start_time = time.time()
    data = json.loads(request.body)
    webhook_code = data['webhook_code']
    webhook_type = data['webhook_type']
    link = data['link_id']

    if (webhook_type == "TRANSACTIONS" and webhook_code in ('new_transactions_available')):
        user_link = UserLink.objects.get(link_id=link)
        transactions = belvo_api.get_transactions(
            link_id=link, days_of_transactions=3)
        belvo_api.addTransactionsToDB(transactions, user_link.user)
        print("--- New Transactions added in %s seconds ---" %
              (time.time() - start_time))

    return Response()


# Deprecated View. This was to make the call as a POST call to Belvo

# @api_view(['POST'])
# def upload_transactions_to_db(request):
#     current_user = request.user
#     user_links = UserLink.objects.filter(user=current_user)
#     if list(user_links) == []:
#         return Response({'abc'},status=status.HTTP_400_BAD_REQUEST)
#     else:
#         for user in user_links:
#             transactions = belvo_api.get_transactions(user.link_id)
#             belvo_api.addTransactionsToDB(transactions, current_user)
#         return Response({'abc'},status=status.HTTP_200_OK)


# @api_view(['GET'])
# def test(request):
#     current_user = User.objects.get(username='jjacosta37@gmail.com')
#     transactions = (Transaction.objects
#         .filter(user_id=current_user, amount=1435.8))
#     print(transactions)
#     return Response('hola')

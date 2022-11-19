from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from fintly import belvo_api

from . import python_functions
from fintly_back.models import Transaction, UserProfile, UserLink

######### API VIEWS #########

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_income_outcome(request):
    current_user = request.user
    month_name = request.GET.get('month')
    month_number = python_functions.return_month(month_name)
    income_date_range = python_functions.return_income_date_range(month_name)
    # TODO: Got to filter by month and year
    income = Transaction.objects.exclude(description__contains='PAGO SUC VIRT TC').filter(transaction_date__month=month_number, user_id=current_user, type='INFLOW').aggregate(income=Sum('amount'))
    expense = Transaction.objects.exclude(description__contains='PAGO SUC VIRT TC').filter(transaction_date__month=month_number, user_id=current_user, type='OUTFLOW').aggregate(outcome=Sum('amount'))
    proyected_savings = 0
    if income['income'] is not None and expense['outcome'] is not None:
        proyected_savings = python_functions.proyect_savings(income['income'], expense['outcome'])

    return Response([income,expense, {'savings':proyected_savings}])


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_expenses_by_category(request):
    month_name = request.GET.get('month')
    month_number = python_functions.return_month(month_name)
    current_user = request.user
    category_groupby = Transaction.objects.exclude(description__contains='PAGO SUC VIRT TC').filter(transaction_date__month=month_number, user_id=current_user, type='OUTFLOW').values(
        'category').order_by('category').annotate(total_price=Sum('amount'))
    return Response(category_groupby)


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def retrieve_update_target_savings(request):
    current_user = request.user
    if request.method == 'GET':
        try:
            user_profile = UserProfile.objects.get(user=current_user)
            ahorro = user_profile.meta_ahorro
        except:
            ahorro = 0
        return Response({"ahorro": ahorro})
    else:
        savings = request.POST.get('savings')
        try:
            user_profile = UserProfile.objects.get(user=current_user)
            user_profile.meta_ahorro = savings
            user_profile.save()
        except:
            user_profile = UserProfile(user=current_user, meta_ahorro=savings)
            user_profile.save()
        return redirect('dashboard')



@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def upload_transactions_to_db(request):
    current_user = request.user
    try:
        user_links = UserLink.objects.filter(user=current_user)
        for user in user_links:
            transactions = belvo_api.getTransactions(user.link_id)
            belvo_api.addTransactionsToDB(transactions, current_user)
    except:
        transactions = {}
    return Response({}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_expenses_by_month(request):
    current_user = request.user
    expenses_by_month = Transaction.objects.exclude(description__contains='PAGO SUC VIRT TC').filter(user_id=current_user, type='OUTFLOW').annotate(month=TruncMonth('transaction_date')).values(
        'month').order_by('month').annotate(total_price=Sum('amount'))
    return Response(expenses_by_month)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_expenses_list_by_month(request):
    month_name = request.query_params.get('month')
    category = request.query_params.get('category')
    month_number = python_functions.return_month(month_name)
    current_user = request.user

    if category == "All":
        expense_list = Transaction.objects.exclude(description__contains='PAGO SUC VIRT TC').filter(
            user_id=current_user, type='OUTFLOW', transaction_date__month=month_number).values().order_by('-amount')
    else:
        expense_list = Transaction.objects.exclude(description__contains='PAGO SUC VIRT TC').filter(
            user_id=current_user, type='OUTFLOW', transaction_date__month=month_number, category__contains=category).values().order_by('-amount')

    return Response(expense_list)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_expenses_category_list(request):
    month_name = request.query_params.get('month')
    month_number = python_functions.return_month(month_name)
    current_user = request.user
    category_list = Transaction.objects.filter(
        user_id=current_user, type='OUTFLOW', transaction_date__month=month_number).values('category').distinct()

    return Response(category_list)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_user_balances(request):
    current_user = request.user
    user_links = UserLink.objects.filter(user=current_user)
    balances = []
    for user in user_links:
        balances.append(belvo_api.get_balances(user.link_id))

    return Response(balances)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_username(request):
    current_user = request.user
    
    if current_user.first_name != "" and current_user.last_name != "":
        username = current_user.first_name + ' ' + current_user.last_name
    else:
        username = current_user.email
    
    return Response(username)
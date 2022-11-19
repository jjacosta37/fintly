from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from fintly_back.models import UserLink

from fintly import belvo_api

######## LOGGED OUT USER VIEWS ##########

######## Home view ###########


def home(request):
    # if request.user.is_authenticated:
    #     return redirect('loading')
    # else:
    return render(request, 'fintly_web/home_home.html')
    

def privacy_policy_screen(request):
    return render(request, 'fintly_web/privacy_policy.html')


######## Auth views ############

def register_user(request):
    if request.method == 'GET':
        return render(request, 'fintly_web/register.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['email'], password=request.POST['password1'],email=request.POST['email'],first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                user.save()
                login(request, user)
                return redirect('dashboard')

            except IntegrityError:
                return render(request, 'fintly_web/register.html', {'form': UserCreationForm, 'error': 'Este usuario ya esta tomado'})
        else:
            return render(request, 'fintly_web/register.html', {'form': UserCreationForm, 'error': 'Ups, parece que las claves que ingresaste no coinciden. Intenta de nuevo!'})
               
def login_user(request):
    if request.method == 'GET':
        return render(request, 'fintly_web/login.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['email'], password=request.POST['password'])
        if user is None:
            return render(request, 'fintly_web/login.html', {'form': AuthenticationForm, 'error': 'Usuario o clave invalida'})
        else:
            login(request, user)
            return redirect('loading')



@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')








######### Belvo widget API Views ###########

@login_required
def belvo_widget(request):
    return render(request, 'fintly_web/belvowidget.html')


@api_view(['GET'])
def generate_token(request):
    token = belvo_api.generateToken()
    return Response(token)


@api_view(['POST'])
def add_link_id(request):
    link = request.data['link']
    institution = request.data['institution']
    current_user = request.user

    if UserLink.objects.filter(link_id=link).exists() is False:
        user_links = UserLink(user=current_user, link_id=link, institution=institution)
        user_links.save()
        # transactions = belvo_api.getTransactions(link)
        # belvo_api.addTransactionsToDB(transactions, current_user)

    return Response(status=status.HTTP_200_OK)



######## DASHBOARD VIEWS ############
@login_required
def dashboard(request):
    current_user = request.user
    if UserLink.objects.filter(user=current_user).exists() is True:
        return render(request, 'fintly_web/dashboard.html')
    elif UserLink.objects.filter(user=current_user).exists() is False:
        return render(request, 'fintly_web/startpage.html')


@login_required
def conntect_new_bank(request):
    return render(request, 'fintly_web/connectaccount.html')


@login_required
def loading(request):
    return render(request, 'fintly_web/loading.html')

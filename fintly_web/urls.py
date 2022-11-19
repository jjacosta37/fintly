from django.urls import path

from . import views

urlpatterns = [ 
               
    # Home and Auth
    path('', views.home, name='home'),
    path('politica-de-privacidad/', views.privacy_policy_screen, name='privacypolicy'),
    path('generatetoken/', views.generate_token, name='generatetoken'),
    path('addlinkid/', views.add_link_id, name='addLinkId'),
    
    # Turned off views. Turn when web version is deployed
    
    # Belvo widget
     # path('belvowidget/', views.belvo_widget, name='belvoWidget'),

    
    # # Auth Views
    
    # path('signup/', views.register_user, name='signupuser'),
    # path('login/', views.login_user, name='loginuser'),
    # path('logout/', views.logout_user, name='logoutuser'),
    
    # # Dashboard views
    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('connectaccount/', views.conntect_new_bank, name='connectAccount'),
    # path('loading/', views.loading, name='loading'),

]

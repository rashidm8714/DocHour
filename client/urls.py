from django.urls import re_path as url
from client import views
# SET THE NAMESPACE!
app_name = 'client'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[

    url(r'login_client/', views.login_client, name='login_client'),
    url(r'signup_client/', views.signup_client, name='signup_client'),
    url(r'register/', views.register, name='register'),
    url(r'user_login/', views.user_login, name='user_login'),
    url(r'client_home/', views.client_home, name='client_home'),
    url(r'book_slot/(?P<slot>\d+)$', views.book_slot, name='book_slot'),
    url(r'delete_slot/(?P<slot>\d+)$', views.delete_slot, name='delete_slot'),
    url(r'^client_home_spec/', views.client_home_spec, name='client_home_spec'),
    url(r'^client_home_doc/', views.client_home_doc, name='client_home_doc'),
    url(r'user_logout/', views.user_logout, name='user_logout')
   
]
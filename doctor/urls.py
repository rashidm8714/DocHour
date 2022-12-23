from django.urls import re_path as url
from doctor import views
# SET THE NAMESPACE!
app_name = 'doctor'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[

    url(r'login_doc/', views.login_doc, name='login_doc'),
    url(r'signup_doc/', views.signup_doc, name='signup_doc'),
    url(r'register/', views.register, name='register'),
    url(r'user_login/', views.user_login, name='user_login'),
    url(r'doc_home/', views.doc_home, name='doc_home'),
    url(r'add_slot/', views.add_slot, name='add_slot'),
    url(r'^doc_home_slot/(?P<date>\d{4}-\d{2}-\d{2})/$', views.doc_home_slot, name='doc_home_slot'),
    url(r'user_logout/', views.user_logout, name='user_logout')
   
]
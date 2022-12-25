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
    url(r'^confirm_booking/(?P<slot>\d+)$', views.confirm_booking, name='confirm_booking'),
    url(r'^cancel_booking/(?P<slot>\d+)$', views.cancel_booking, name='cancel_booking'),
    url(r'^delete_slot/(?P<slot>\d+)$', views.delete_slot, name='delete_slot'),
    url(r'^doc_home_slot/(?P<date>\d{4}-\d{2}-\d{2})/$', views.doc_home_slot, name='doc_home_slot'),
    url(r'^doc_home_chat/(?P<client>\d+)$', views.doc_home_chat, name='doc_home_chat'),
    url(r'^doc_home_send/(?P<client>\d+)$', views.doc_home_send, name='doc_home_send'),
    url(r'delete_msg/', views.delete_msg, name='delete_msg'),
    url(r'user_logout/', views.user_logout, name='user_logout')
   
]
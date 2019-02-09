from django.urls import path

from test01 import views

app_name = 'test01'

urlpatterns = [
    path('login/', views.login, name='login'),
]


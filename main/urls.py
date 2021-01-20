from django.urls import path
from . import views

urlpatterns = [
    path('', views.BaseView.as_view(), name='base'),
    path('forms/<str:slug>/<str:stage>', views.FormsView.as_view(), name='forms'),

]

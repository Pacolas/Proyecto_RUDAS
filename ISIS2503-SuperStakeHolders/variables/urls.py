from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('variables/', views.solicitar_tarjeta),
    path('variablecreate/', csrf_exempt(views.variable_create), name='variableCreate'),
    path('variablesAdmin/', views.variable_list, name='variableList'),
    path('variablesshow/', views.variable_list2, name='variablesShow')
]
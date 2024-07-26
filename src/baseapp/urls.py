from django.urls import path
from . import views

app_name = 'baseapp'
urlpatterns = [
    path("", views.Visualizer.home_page),
    path("trades/", views.Visualizer.display_trades, name='trades')
]

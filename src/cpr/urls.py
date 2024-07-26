from django.urls import path
from . import views

urlpatterns = [
    path('', views.execute),
    # path("handle_trade/<path:filepath>/<str:datetime>/", views.handle_trade, name='handle_trade')
    # path('chart/<str:start_date>/<str:entry_date_time>/<str:exit_date_time>/<str:cpr_high>/<str:cpr_low>/', views.ChartView.display_chart, name='display_chart')
]

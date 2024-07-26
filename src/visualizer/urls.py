from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_file, name="upload_file"),
    path("handle_trade/<path:filepath>/<str:datetime>/", views.handle_trade, name='handle_trade')
]

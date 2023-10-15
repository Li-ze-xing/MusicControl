from django.urls import path, re_path

from app import views
from app.views import Charts

urlpatterns = [
    path('charts/', Charts.as_view(), name='charts'),
]
                                
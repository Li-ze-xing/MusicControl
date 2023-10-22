from django.urls import path, re_path
from  .views import Index1,Index2,Index3,Index4





urlpatterns = [
    path("index1/",Index1.as_view()),
    path("index2/",Index2.as_view()),
    path("index3/",Index3.as_view()),
    path("index4/",Index4.as_view()),
]
                                
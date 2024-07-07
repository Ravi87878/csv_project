from django.contrib import admin
from django.urls import path,include
from .views import CSVQueryView
urlpatterns = [
    path('upload-csv/',CSVQueryView.as_view()),
    path('<int:pk>/',CSVQueryView.as_view())
]
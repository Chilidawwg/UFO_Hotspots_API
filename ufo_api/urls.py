from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ufo_api import views

urlpatterns = [
    path('ufo_api/', views.UFOData.as_view()),
    path('ufo_api/<int:pk>/', views.UFODataDetails.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)

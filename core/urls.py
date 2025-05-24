from django.urls import path
from . import views
urlpatterns = [
     path('query/',views.get_answer, name = "get_answer"),
     path('parse-image/', views.parse_image, name = "parse_image")
]

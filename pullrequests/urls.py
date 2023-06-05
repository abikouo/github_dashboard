from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("<str:repository_name>/", views.display, name="display"),
]
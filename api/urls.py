from django.urls import path

from .views import aks, AKDetailView, comments

urlpatterns = [
    path('aks/<int:pk>/comments/', comments),
    path('aks/<int:pk>/', AKDetailView.as_view()),
    path('aks/', aks),
]


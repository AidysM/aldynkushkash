from django.urls import path
from .views import other_page
from .views import index, AKLoginView

app_name = 'main'
urlpatterns = [
    path('accounts/login/', AKLoginView.as_view(), name='login'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]
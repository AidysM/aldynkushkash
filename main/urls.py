from django.urls import path
from .views import other_page
from .views import index, AKLoginView, profile, AKLogoutView

app_name = 'main'
urlpatterns = [
    path('accounts/logout/', AKLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', AKLoginView.as_view(), name='login'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]
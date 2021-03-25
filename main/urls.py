from django.urls import path
from .views import other_page
from .views import index, AKLoginView, profile, AKLogoutView, ChangeUserInfoView, AKPasswordChangeView

app_name = 'main'
urlpatterns = [
    path('accounts/logout/', AKLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', AKPasswordChangeView.as_view(), name='password_change'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', AKLoginView.as_view(), name='login'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]
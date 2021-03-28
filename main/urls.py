from django.urls import path
from .views import other_page, RegisterUserView, RegisterDoneView, user_activate, DeleteUserView
from .views import index, AKLoginView, profile, AKLogoutView, ChangeUserInfoView, AKPasswordChangeView
from .views import by_rubric, detail, profile_ak_detail, profile_ak_add
from .views import profile_ak_change, profile_ak_delete

app_name = 'main'
urlpatterns = [
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/logout/', AKLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', AKPasswordChangeView.as_view(), name='password_change'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/change/<int:pk>/', profile_ak_change, name='profile_ak_change'),
    path('accounts/profile/delete/<int:pk>/', profile_ak_delete, name='profile_ak_delete'),
    path('accounts/profile/add/', profile_ak_add, name='profile_ak_add'),
    path('accounts/profile/<int:pk>/', profile_ak_detail, name='profile_ak_detail'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', AKLoginView.as_view(), name='login'),
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]

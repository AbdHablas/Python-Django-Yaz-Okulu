from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='user_index'),
    path('logout/', views.logout_view, name='logout_view'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup_views'),
    path('password/', views.user_password, name='user_password'),
    path('update/', views.user_update, name='user_update'),

]

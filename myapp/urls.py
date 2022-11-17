from django.urls import path
from myapp import views


# URL patterns here


urlpatterns = [
    path('',views.index, name="index"),
    path('login/',views.login_user, name="login"),
    path('register/',views.register_user, name="register"),
    path('logout', views.logout_user, name="logout"),
    path('profile', views.profile, name="profile"),
]

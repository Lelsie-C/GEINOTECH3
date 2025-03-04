from django.urls import path
from .views import login_view, main_page

urlpatterns = [
    path("", login_view, name="login"),
    path("main/", main_page, name="main"),
]

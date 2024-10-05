from django.urls import path
from.import views
urlpatterns = [

   

path('', views.login_view , name = "login_view" ),
path('logout_view', views.logout_view , name = "logout_view" ),

]
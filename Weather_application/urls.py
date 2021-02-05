from django.urls import path

from . import views

# Connect the functions from views.py to the url paths
urlpatterns = [
    path('', views.pag1, name='home'),
    path('Index/', views.pag1, name='home'),
    path('current_city/', views.filled_in_current_weather, name='current_weather'),
    path('forecast_city/', views.filled_in_weather_forecast, name='forecast_weather'),
    path('forecast/', views.forecast, name='weekly-forecast'),
    path('rain/', views.rain, name='rain'),
    path('rain_city/', views.filled_in_rain, name='rain_city'),
    path('current_city/not_found/', views.page_not_found, name='Place_not_found'),
    path('forecast_city/not_found/', views.page_not_found, name='Place_not_found'),
    path('rain_city/not_found/', views.page_not_found, name='place_not_found'),
]

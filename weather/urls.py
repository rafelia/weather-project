from django.urls import path
from . import views

urlpatterns = [
    path('latest_forecast/', views.CurrentWeatherData.as_view(), name='current-weather'),
    path('average_forecast/', views.ForecastWeatherData.as_view(), name='forecast-weather'),
    path('top_metrics/<int:nparameter>/', views.top3citiesmetrics.as_view(), name='historical-weather'),
]

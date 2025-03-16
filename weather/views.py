from rest_framework import generics
from .models import WeatherData
from .serializers import WeatherDataSerializer, AggregatedWeatherDataSerializer, RankMetricsSerializer
from django.db import connection
from django.db.models import OuterRef, Subquery
from django.db.models import F, Window, DateField, Avg
from django.db.models.functions import Cast, RowNumber, ExtractHour
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import generics


class CurrentWeatherData(generics.ListAPIView):
    serializer_class = WeatherDataSerializer

    def get_queryset(self):

        queryset = WeatherData.objects.annotate(

            date=Cast('Datetime', DateField())
        ).annotate(

            rn=Window(
                expression=RowNumber(),
                partition_by=[F('country'), Cast('Datetime', DateField())],
                order_by=ExtractHour('Datetime').desc()
            )
        ).filter(
            rn=1  
        ).order_by('Datetime', 'country')
        return queryset

class ForecastWeatherData(generics.ListAPIView):
    serializer_class = AggregatedWeatherDataSerializer

    def get_queryset(self):
        subquery = WeatherData.objects.annotate(
            date=Cast('Datetime', DateField())
        ).annotate(
            rn=Window(
                expression=RowNumber(),
                partition_by=[F('country'), F('date')],
                order_by=F('Datetime').desc()
            )
        ).filter(
            rn__gte=3  
        ).values('country', 'date', 'temperature')

        queryset = WeatherData.objects.annotate(
            date=Cast('Datetime', DateField())
        ).filter(
            id__in=Subquery(subquery.values('id')) 
        ).values('country', 'date').annotate(
            avg_temp=Avg('temperature')
        ).order_by('date', 'country')  

        return queryset

class top3citiesmetrics(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        nparameter = self.kwargs.get('nparameter')
        if nparameter:
            nparameter = int(nparameter)
            qs_dict = {}
            final_qs = {}
            list_dict = [
                'temperature','max_temp_2m','wind_speed','precipitation',
                'pressure','wind_direction','wind_gusts_10m','humidity',
                'weather_symbol_1h','UV_index'
            ]

            for metric in list_dict:
                qs_dict[metric] = WeatherData.objects.annotate(
                    rank=Window(
                        expression=RowNumber(),
                        partition_by=[F('country')],
                        order_by=F(metric).desc()
                    )
                ).filter(rank=1).order_by('-' + metric)[:nparameter]

                final_qs[metric] = [
                    {
                        "location": item.country.city if item.country else "Unknown", 
                        "value": getattr(item, metric)
                    }
                    for item in qs_dict[metric]
                ]
            return Response(final_qs)
                

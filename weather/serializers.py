from rest_framework import serializers
from .models import WeatherData, CountryData

class CountryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryData
        fields = ['country', 'city', 'lon', 'lat']

class WeatherDataSerializer(serializers.ModelSerializer):
    country = CountryDataSerializer(read_only=True)

    class Meta:
        model = WeatherData
        fields = [
            'Datetime', 'temperature', 'max_temp_2m', 'wind_speed',
            'precipitation', 'pressure', 'wind_direction', 'wind_gusts_10m',
            'humidity', 'weather_symbol_1h', 'UV_index', 'country'
        ]

    def to_representation(self, instance):
        # Get the original representation
        rep = super().to_representation(instance)
        # Flatten the country field if it exists
        country_data = rep.pop('country', None)
        if country_data:
            rep.update(country_data)
        return rep




class AggregatedWeatherDataSerializer(serializers.Serializer):
    date = serializers.DateField()
    avg_temp = serializers.FloatField()
    country = serializers.SerializerMethodField()

    def get_country(self, obj):
        # Fetch the CountryData instance using the country ID
        country_id = obj['country']
        country_instance = CountryData.objects.get(id=country_id)
        return CountryDataSerializer(country_instance).data

    
    def to_representation(self, instance):
        # Get the original representation
        rep = super().to_representation(instance)
        # Flatten the country field if it exists
        country_data = rep.pop('country', None)
        if country_data:
            rep.update(country_data)
        return rep


        


class RankMetricsSerializer(serializers.ModelSerializer):
    country = CountryDataSerializer(read_only=True)

    class Meta:
        model = WeatherData
        fields = '__all__'

    def to_representation(self, instance):
        # Get the original representation
        rep = super().to_representation(instance)
        # Flatten the country field if it exists
        country_data = rep.pop('country', None)
        if country_data:
            rep.update(country_data)
        return rep
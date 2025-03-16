from django.db import models

class CountryData(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default='Unknown')
    lon = models.CharField(max_length=15)
    lat = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)


class WeatherData(models.Model):
    Datetime = models.DateTimeField()
    #lon = models.CharField(max_length=15)
    #lat = models.CharField(max_length=15)
    temperature = models.FloatField()
    max_temp_2m = models.FloatField()
    wind_speed = models.FloatField()
    precipitation = models.FloatField()
    pressure = models.FloatField()
    wind_direction = models.FloatField()
    wind_gusts_10m = models.FloatField()
    humidity = models.FloatField(default=0)
    weather_symbol_1h = models.FloatField()
    UV_index = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.ForeignKey(CountryData, on_delete=models.CASCADE, null=True, blank=True)


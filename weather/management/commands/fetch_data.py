import datetime as dt
import os
import pandas as pd
from datetime import datetime

import meteomatics.api as api
from django.core.management.base import BaseCommand
from weather.models import WeatherData, CountryData

class Command(BaseCommand):
    help = 'Fetch weather data and populate the WeatherData table'

    def handle(self, *args, **options):
        
        
        CountryData.objects.create(country='England', city='London', lon='-0.13', lat='51.51')
        CountryData.objects.create(country='Greece', city='Athens', lon='23.73', lat='37.98')
        CountryData.objects.create(country='Cyprus', city='Paphos', lon='32.42', lat='34.77')

        username = os.environ["MeteoUser"]
        password = os.environ["MeteoPwd"]

        # The API expects coordinates as (lat, lon) tuples.
        coordinates = [(51.51, -0.13), (37.98, 23.73), (34.77, 32.42)]
        parameters = [
            't_2m:C', 't_max_2m_24h:C', 'wind_speed_10m:ms',
            'precip_1h:mm', 'msl_pressure:hPa', 'wind_dir_10m:d',
            'wind_gusts_10m_1h:ms', 'absolute_humidity_2m:gm3',
            'weather_symbol_1h:idx', 'uv:idx'
        ]
        model = 'mix'
        currentdate = dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        startdate = currentdate + dt.timedelta(days=1)
        enddate = currentdate + dt.timedelta(days=7)
        enddate = enddate.replace(hour=23, minute=0, second=0, microsecond=0)
        
        interval = dt.timedelta(hours=1)

        df = api.query_time_series(coordinates, startdate, enddate, interval, parameters, username, password, model=model)
        df.reset_index(inplace=True)

        weather_data_objects = []

        for index, row in df.iterrows():
            # Convert the validdate to a datetime object.
            try:
                valid_date = datetime.fromisoformat(row['validdate'])
            except Exception:
                valid_date = pd.to_datetime(row['validdate'])

            # Convert API-returned coordinates to strings.
            # (Ensure these match the values stored in CountryData.)
            lon = str(row['lon'])
            lat = str(row['lat'])
            
            try:
                # Look up the CountryData record based on matching lon and lat.
                country_id  = CountryData.objects.filter(lon=lon, lat=lat).values_list('id', flat=True).first()
            except CountryData.DoesNotExist:
                country_id  = None
            
            wd = WeatherData(
                Datetime=valid_date,
                #lon=lon,
                #lat=lat,
                temperature=row['t_2m:C'],
                max_temp_2m=row['t_max_2m_24h:C'],
                wind_speed=row['wind_speed_10m:ms'],
                precipitation=row['precip_1h:mm'],
                pressure=row['msl_pressure:hPa'],
                wind_direction=row['wind_dir_10m:d'],
                wind_gusts_10m=row['wind_gusts_10m_1h:ms'],
                humidity=row['absolute_humidity_2m:gm3'],
                weather_symbol_1h=row['weather_symbol_1h:idx'],
                UV_index=row['uv:idx'],
                country_id =country_id 
            )
            weather_data_objects.append(wd)

        WeatherData.objects.bulk_create(weather_data_objects)
        self.stdout.write(self.style.SUCCESS('Weather data fetched and saved successfully!'))

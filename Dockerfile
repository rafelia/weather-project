FROM python:3.9

ARG METEOUSER
ARG METEOPWD
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV MeteoUser=$METEOUSER
ENV MeteoPwd=$METEOPWD

WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/

RUN python manage.py migrate --noinput
RUN python manage.py fetch_data

EXPOSE 8080
CMD ["gunicorn", "weather_project.wsgi:application", "--bind", "0.0.0.0:8080"]

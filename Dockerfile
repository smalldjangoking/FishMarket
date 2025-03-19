FROM python:3.9-slim

WORKDIR /app
COPY /FishMarket /app/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY Pipfile Pipfile.lock /app/
RUN pip install --no-cache-dir pipenv && pipenv install --deploy --system
EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py createsuperuser --noinput --email $DJANGO_SUPERUSER_EMAIL || true && python manage.py runserver 0.0.0.0:8000"]
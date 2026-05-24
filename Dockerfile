FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $PORT

CMD sh -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn erp_v2.wsgi:application --bind 0.0.0.0:$PORT"
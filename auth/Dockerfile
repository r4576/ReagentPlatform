FROM python:3.8.5
WORKDIR /app/auth
COPY . .
RUN pip install -r requirements.txt
CMD python manage.py runserver 172.20.0.3:8080
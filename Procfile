release: python3 manage.py makemigrations && python3 manage.py migrate
web: daphne diploma_project.asgi:application --port $PORT --bind 0.0.0.0 -v2

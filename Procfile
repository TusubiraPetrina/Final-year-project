init: python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py createsuperuser --username admin --email finalyear@project.com --no_input
upgrade: python3 manage.py migrate
web: gunicorn server.wsgi
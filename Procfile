init: python3 manage.py db init && python3 manage.py db migrate && python3 manage.py db upgrade
upgrade: pip install -r requirements.txt && python3 manage.py db upgrade
create_defaults: python3 manage.py create_defaults
web: gunicorn server.wsgi
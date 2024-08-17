web: gunicorn pdf_converter.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn pdf_converter.wsg
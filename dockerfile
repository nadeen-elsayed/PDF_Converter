FROM python:3.12
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
# Collect static files
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN python manage.py collectstatic --noinput
# Expose the port the app runs on
EXPOSE 7000
CMD ["python", "manage.py", "runserver", "0.0.0.0:7000"]

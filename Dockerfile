# pull official base image
FROM python:3.8.0-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#COPY . /usr/src/app/
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=127.0.0.1

COPY ./requirements.txt requirements.txt
#RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"

RUN pip install -r requirements.txt 

# copy project

COPY . .

EXPOSE 5000

#CMD ["python3", "test_isi.py"]

ENTRYPOINT sh docker-entrypoint.sh test 

FROM python:3.7-alpine
RUN pip install --upgrade pip
COPY requirements.txt /srv/requirements.txt
RUN pip install -r /srv/requirements.txt
ENV FLASK_APP=app
WORKDIR /srv
COPY . /srv
CMD python -m flask run -p 8080 -h 0.0.0.0

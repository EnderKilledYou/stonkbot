FROM nikolaik/python-nodejs:python3.7-nodejs16-bullseye
RUN pip install --upgrade pip
COPY requirements.txt /srv/requirements.txt
RUN pip install -r /srv/requirements.txt
ENV FLASK_APP=app
WORKDIR /srv
COPY . /srv
RUN npm install
RUN npm run build
CMD python -m flask run -p 80 -h 0.0.0.0
#9,223,372,036,854,775,807
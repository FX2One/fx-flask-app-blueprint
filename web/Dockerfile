FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /market
WORKDIR /market
COPY requirements.txt /market/
RUN pip install -r requirements.txt
COPY . /market/
#CMD ["flask","run"]
#CMD gunicorn -bind 0.0.0.0:5000 -w 3 run:app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]

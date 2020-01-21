FROM python:3

COPY . /

RUN pip install flask rethinkdb

CMD [ "sh", "-c", "/start.sh"]

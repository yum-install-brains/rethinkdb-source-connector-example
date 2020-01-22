FROM python:3

COPY . /

RUN pip --disable-pip-version-check install flask rethinkdb

CMD [ "sh", "-c", "/start.sh"]

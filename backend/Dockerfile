
FROM python:3.10-alpine

#WORKDIR /usr/Esummit23-backend

ENV PYTHONBUFFERED 0

# install psycopg2 dependencies for postgres
# RUN apk update \
#   && apk add postgresql-dev gcc python3-dev musl-dev build-base py-pip jpeg-dev zlib-dev xvfb fontconfig ttf-freefont ffmpeg libwebp libwebp-tools libwebp-dev

# RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev



RUN pip install --upgrade pip \
  && pip install --upgrade setuptools \
  && pip install --upgrade pipenv  \
  && pip install --upgrade boto3 \
  && pip install --upgrade django-storages \
  && pip install gevent

#  && pip install psycopg2


COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /usr/backend
WORKDIR /usr/backend

COPY . .

CMD ["sh", "-c", "python manage.py collectstatic --no-input; python manage.py migrate;gunicorn backend.wsgi:application -b 0.0.0.0:8009"]
FROM selenium/standalone-chrome:3.141.59

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Kiev

USER root


RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /code

RUN apt-get update && apt-get -y install python3 python3-pip
RUN rm -f /usr/bin/pip

RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN apt-get update && apt-get install -y python3-gdbm


COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

USER seluser

COPY . .

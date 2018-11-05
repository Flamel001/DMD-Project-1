FROM python:3.6

RUN pip install --upgrade pip


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gettext && \
    apt-get clean

#EXPOSE 8000

WORKDIR /app

ADD ./requirements.txt .
RUN pip install -r requirements.txt

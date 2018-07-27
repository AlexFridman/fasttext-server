from python:3

MAINTAINER alexfridman@outlook.com

# to speedup building
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -U -r requirements.txt


COPY . /app
WORKDIR /app

ENTRYPOINT ["python", "bin/sberbot-nlu-back"]

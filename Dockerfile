from python:3

MAINTAINER daniel@federschmidt.xyz

# to speedup building
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -U -r requirements.txt


COPY . /app
WORKDIR /app




ENTRYPOINT ["python", "bin/bot-back"]

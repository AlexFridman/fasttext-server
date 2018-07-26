from python:3

MAINTAINER daniel@federschmidt.xyz

COPY . /app
WORKDIR /app

RUN pip install pipenv
RUN pipenv install --system
RUN pip install .

ENTRYPOINT ["python", "ft_server/__main__.py"]

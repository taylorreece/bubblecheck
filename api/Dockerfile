FROM ubuntu:latest

# Install some apt packages
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential libpq-dev

# Install some pip packages
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

# Copy up our application
COPY . /app
WORKDIR /app

ENV FLASK_DEBUG=true
ENV LC_ALL=C.UTF-8
ENV LC_ALL=C.UTF-8

ENTRYPOINT ["python3"]
CMD ["run.py"]

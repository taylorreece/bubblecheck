FROM python:3-alpine

RUN apk update && apk add build-base postgresql-dev gcc python3-dev musl-dev zlib-dev jpeg-dev

# Install some pip packages
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy up our application
COPY . /app
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["run.py"]

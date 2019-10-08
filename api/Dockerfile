FROM python:3-alpine
RUN apk update && \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev

# Install some pip packages
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Remove build requirements for postgresql; slim down the image
RUN apk --purge del .build-deps

# Copy up our application
COPY . /app
WORKDIR /app

ENTRYPOINT ["python", "run.py"]

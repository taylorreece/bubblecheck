FROM python:3-alpine

# Install some pip packages
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy up our application
COPY . /app
WORKDIR /app

ENTRYPOINT ["python", "run.py"]

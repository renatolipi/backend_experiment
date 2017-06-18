FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y  python-dev python-pip python-virtualenv git curl build-essential
RUN pip install -U pip

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# run webserver
ENTRYPOINT ["gunicorn" "company_project.wsgi"]

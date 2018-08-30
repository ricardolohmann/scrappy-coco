FROM python:3.6

WORKDIR /code

COPY requirements.txt /code

RUN pip install -r requirements.txt

COPY . /code

WORKDIR /code/scrappy_coco
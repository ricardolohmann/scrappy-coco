# scrappy-coco

The project is composed by two services:
- app:
    The service which runs Scrapy and make it available by using ScrapyRT.
- telegram:
    The service that get messages in Telegram bot by pulling.



Contributing
============

Install development dependencies:
```shell
pip install -r requirements-dev.txt
```
then run `docker-compose`


Running
=======

Starting containers:
```shell
docker-compose up --build
```

It's also possible to consume Scrapy thrue HTTP request, like the following:
```shell
curl -v "http://localhost:9080/crawl.json?url=http://old.reddit.com/r/cats&spider_name=reddit" | jq
```
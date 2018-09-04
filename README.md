# scrappy-coco

Running
=======

Start container
```shell
docker-compose up --build
```


Run different commands in container
```shell
docker run scrappycoco_app scrapy crawl reddit -o reddit.json -a subreddits=cats;brazil;worldnews
```
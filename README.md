# IMDB Scrapy Crawling

Project using Scrapy to crawl through IMDB website for 500 movies of each genre.

## Extracted data

This project extracts movies titles, ratings, and its genre - depending on the page in which it is shown in the IMDB website. The movies are extracted to different JsonLines files based on their genre, and ordered by movie rating. The data of each movie extracted looks like this sample:

{"title": "A Series of Unfortunate Events", "rating": "7.9", "genre": "Comedy"}

## Running the Movies spider

You can run the movies spider using the ```scrapy crawl``` command:

```
$ scrapy crawl movies
```

## Setup

In case you don't have Scrapy installed, you can install it through Anaconda or Pip. I recommend using Anaconda as it provides a easy way to open a different environment to run Scrapy.

1. Download Anaconda at ```https://www.anaconda.com/download/``` and install it.
2. Create a environment and install Scrapy on it.
3. Run the enviroment with the command ```source activate ENVIRONMENT-NAME``` (on macOS), or ```activate ENVIRONMENT-NAME```(for windows)
4. Run the ```scrapy crawl SPIDER-NAME``` (movies in this case) command.

## Scrapy Guides

You can learn more about Scrapy and Spiders by going through the Scrapy documentation:
```https://doc.scrapy.org/en/latest/index.html```
import scrapy

from imdb_movies.items import MovieItem

class MoviesSpider(scrapy.Spider):
  name = 'movies'
  allowed_domains = ['imdb.com']
  start_urls = ['https://www.imdb.com/feature/genre/']

  def parse(self, response):
    i = 1
    pages = 1
    genre_links = response.xpath('//div[@class="widget_image"]/div[@class="image"]/a/@href').extract()
    # for each genre in the genre page, call parse_genres to order by rating and then parse each movie
    for genre in genre_links:
      if(i <= len(genre_links)):
        i = i + 1
        yield response.follow(genre, self.parse_pages, meta={'pages': pages})

  # call parse_movies for each movie of the FIRST page
  def parse_pages(self, response):
    movies_links = response.xpath('//div[@class="lister-item-content"]/h3[@class="lister-item-header"]/a/@href').extract()
    movie_genre = response.xpath('//h1[@class="header"]/text()').extract_first().split()[2]
    next_page = response.xpath('//a[@class="lister-page-next next-page"]/@href').extract_first()
    pages = response.meta['pages']

    for movie in movies_links:
      yield response.follow(movie, self.parse_movies, meta={'movie_genre': movie_genre})

    # If there is a next_page link, follow it to keep scraping more movies
    if next_page is not None:
      # limit of 10 pages scraped per movie genre to scrape 500 movies
      if(pages < 10):
        pages = pages + 1
        yield response.follow(next_page, self.parse_pages, meta={'pages': pages})

  # parse movie data from movie page
  def parse_movies(self, response):
    movie = MovieItem()

    # Extract movie data: movie title, rating, and genre (genre page in which it is displayed)
    # It is possible to scrape other movie data if necessary
    movie['title'] = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract_first().strip()
    movie['rating'] = response.xpath('//div[@class="ratingValue"]/strong/span/text()').extract_first()
    movie['genre'] = response.meta['movie_genre']

    return movie
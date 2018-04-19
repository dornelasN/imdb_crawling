import scrapy

from imdb_movies.items import MovieItem

class MoviesSpider(scrapy.Spider):
  name = 'movies'
  allowed_domains = ['imdb.com']
  start_urls = ['https://www.imdb.com/feature/genre/']
  movies_list = []

  def parse(self, response):
    i = 1
    genre_links = response.xpath('//div[@class="widget_image"]/div[@class="image"]/a/@href').extract()
    # for each genre in the genre page, call parse_genres to order by rating and then parse each movie
    for genre in genre_links:
      if(i <= len(genre_links)):
        i = i + 1
        yield response.follow(genre, self.parse_pages)

# follow website link to order movies by user_rating
#  def parse_rating(self, response):
#    rating_link = response.xpath('//div[@class="sorting"]/a[@class="user_rating"]/@href').extract_first()
#    yield response.follow(rating_link, self.parse_pages)

  # call parse_movies for each movie of the FIRST page
  def parse_pages(self, response):
    movies_links = response.xpath('//div[@class="lister-item-content"]/h3[@class="lister-item-header"]/a/@href').extract()
    movie_genre = response.xpath('//h1[@class="header"]/text()').extract_first().split()[2]

    for movie in movies_links:
      yield response.follow(movie, self.parse_movies, meta={'movie_genre': movie_genre} )

  # parse movie data from movie page
  def parse_movies(self, response):
    movie = MovieItem()

    movie['title'] = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract_first().strip()
    movie['rating'] = response.xpath('//div[@class="ratingValue"]/strong/span/text()').extract_first()
    movie['genre'] = response.meta['movie_genre']
    # movie['genres'] = response.xpath('//div[@class="subtext"]/a/span[@itemprop="genre"]/text()').extract()

    return movie
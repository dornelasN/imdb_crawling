# Test output files to check if data is organized by Rating and if the output contains 500 JSON movie objects
# Should be run only after Scrapy has crawled through IMDB and output files have been generated!
# run command: python test_movies_spider.py

import json

movie_genres = ['\"superhero\"', 'Action-Comedy', 'Action', 'Adventure', 'Comedy-Romance', 'Comedy', 'Crime', 'Drama', 'Fantasy', 'Horror', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller']

for genre in movie_genres:
  movies_list = list()
  with open('%s.jsonl' % genre, 'r') as file:
    for line in file:
      movies_list.append(json.loads(line))

  print(genre + ' list is ' + str(len(movies_list)) + ' movies long.')

  ordered = True
  for index in range( len(movies_list) -1):
    try:
      if(float(movies_list[index]['rating']) < float(movies_list[index+1]['rating'])):
        ordered = False
    except TypeError:
        oredered = True
        # print(str(movies_list[index]['rating']) + ' < ' + str((movies_list[index+1]['rating'])) + '?')

  print(genre + ' movies is ordered? - ' + str(ordered) + '\n')
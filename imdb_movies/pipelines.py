# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exporters import JsonLinesItemExporter

class PerRatingJsonLinesExportPipeline(object):
    def open_spider(self, spider):
        self.genre_to_exporter = {}
        self.files_to_order = []

    def close_spider(self, spider):
        for exporter in self.genre_to_exporter.values():
            exporter.finish_exporting()
            exporter.file.close()

        for genre_file in self.files_to_order:
            self.reorder_file(genre_file)

    def _exporter_for_item(self, item):
        genre = item['genre']
        self.files_to_order.append(genre)
        if genre not in self.genre_to_exporter:
            file = open('%s.jsonl' % genre, 'ab')
            exporter = JsonLinesItemExporter(file)
            exporter.start_exporting()
            self.genre_to_exporter[genre] = exporter
        return self.genre_to_exporter[genre]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item

    def reorder_file(self, filename):
        list_to_order = list()
        # Extract rating from json Object, return 0 if TypeError is raised (rating == null)
        def extract_rating(json):
            try:
                return float(json['rating'])
            except TypeError:
                return 0

        # open json file and append every line (JSON objects) to a list
        with open('%s.jsonl' % filename, 'r') as file:
            for line in file:
                list_to_order.append(json.loads(line))
        file.close()

        # sort the list of JSON objects by rating
        list_to_order.sort(key = extract_rating, reverse = True)

        # write the list of sorted JSON objects back to the file, overwritting its previous content
        with open('%s.jsonl' % filename, 'w') as file:
            for item in list_to_order:
                file.write(json.dumps(item) + '\n')
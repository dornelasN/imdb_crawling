# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter

class PerRatingJsonLinesExportPipeline(object):
    def open_spider(self, spider):
        self.genre_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.genre_to_exporter.values():
            exporter.finish_exporting()
            exporter.file.close()

    #TODO: re order the movies by Rating
    def _exporter_for_item(self, item):
        genre = item['genre']
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
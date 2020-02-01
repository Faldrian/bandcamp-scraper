# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class BandcampPipeline(object):

    def process_item(self, item, spider):
        license_url = None

        if ("all rights reserved" in item['license'][0]):
            license = 0  # Commercial
        else:
            if ('license_url' in item):
                license = 1  # One license for the whole album
                license_url = item['license_url'][0]
            else:
                license = 2  # Individual licenses per track

        title = item['title'][0].strip()
        artist = item['artist'][0].strip()

        spider.cur.execute("insert into album values (?, ?, ?, ?, ?, ?)",
            (item['album_url'][0], title, artist,
             license_url, license, item['numsongs'][0]))

        return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class BandcampPipeline(object):

    def process_item(self, item, spider):
        license = 0 if ("all rights reserved" in item['license'][0]) else 1
        license_url = item['license_url'][0] if license == 1 else None

        title = item['title'][0].strip()
        artist = item['artist'][0].strip()

        spider.cur.execute("insert into album values (?, ?, ?, ?, ?, ?)",
            (item['album_url'][0], title, artist,
             license_url, license, item['numsongs'][0]))

        return item

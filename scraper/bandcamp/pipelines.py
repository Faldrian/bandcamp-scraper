# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import datetime

class BandcampPipeline(object):

    def process_item(self, item, spider):
        license_url = None

        if "all rights reserved" in item['license'][0]:
            license = 0  # Commercial
        else:
            if 'license_url' in item:
                license = 1  # One license for the whole album
                license_url = item['license_url'][0]
            else:
                license = 2  # Individual licenses per track

        spider.albumdb.save({
            'album_url': item['album_url'][0],
            'license': license,
            'license_url': license_url,
            'tags': item['tags'],
            'numsongs': item['numsongs'][0],
            'album_json': item['album_json'][0],
            'tracks_json': item['tracks_json'][0],
            'crawltime': datetime.datetime.now().isoformat()
        })

        return item

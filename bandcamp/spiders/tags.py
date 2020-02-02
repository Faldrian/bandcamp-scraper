import json
import re
import scrapy
import logging
import couchdb
from scrapy.loader import ItemLoader
from bandcamp.items import Album


class TagSpider(scrapy.Spider):
    albumdb = None

    name = "tags"
    formatstring = '{"filters":{"format":"all","location"' + \
                   ':0,"sort":"pop","tags":["%s"]},"page":%d}'

    def start_requests(self):
        # First thing: connect to database
        # (can't be done in constructor, because self.settings is set later)
        couch = couchdb.Server()

        # create or use existing database
        if 'album' in couch:
            self.albumdb = couch['album']
        else:
            self.albumdb = couch.create('album')

        tag = 'electronic'
        page = 1

        yield self.create_hub_request(tag, page)


    def parse_dig_deeper(self, response, tag, page):
        json_blob = json.loads(response.body)

        items = json_blob['items']
        more_available = json_blob['more_available']

        for item in items:
            album_url = item['tralbum_url']

            # Only scrape the album if we don't already know it
            docs = list(self.albumdb.find(
                {'selector': {'album_url': album_url}}))
            num_rows = len(docs)

            if num_rows == 0:
                logging.info("Crawling new Album: %s", album_url)
                yield scrapy.Request(url=album_url,
                                     callback=self.parse_album,
                                     cb_kwargs=dict(album_json=item))
            else:
                logging.info("Skipping known Album: %s", album_url)

        if(more_available and page < 1):
            logging.info("More available, loading next page: %d.", (page + 1))
            yield self.create_hub_request(tag, page + 1)
        else:
            logging.info("No more available or page limit reached." \
                         "Last page: %d", page)


    def create_hub_request(self, tag, page):
        requestbody = self.formatstring % (tag, page)

        return scrapy.Request(
            url='https://bandcamp.com/api/hub/2/dig_deeper',
            method='POST',
            body=requestbody,
            callback=self.parse_dig_deeper,
            cb_kwargs=dict(tag=tag, page=page))


    def parse_album(self, response, album_json):
        loader = ItemLoader(item=Album(), response=response)
        loader.add_value('album_url', response.url)
        loader.add_css('license', '#license')
        loader.add_css('license_url', '#license a.cc-icons::attr(href)')
        loader.add_css('tags', '.tralbum-tags .tag::text')

        numsongs = len(response.css('#track_table [itemprop="tracks"]'))
        loader.add_value('numsongs', numsongs)
        loader.add_value('album_json', album_json)

        # get trackinfos (extract from javascript-block)
        jsblock = response.css('#pgBd > script:nth-child(4)::text').get()
        loader.add_value('tracks_json', self.extract_track_data(jsblock))

        return loader.load_item()


    def extract_track_data(self, jsblock):
        # get the general textblock (excluding leading comments)
        infostart = jsblock.find('TralbumData = {')
        infostart = jsblock.find('    current: {', infostart)  # no comments
        infoend = jsblock.find('};', infostart) + 1  # to include "}"
        jsdata = jsblock[infostart:infoend]

        # put property names in quotes
        sanatized = re.sub(r'\s{4}([a-zA-Z_]+)\:\s', r'    "\1": ', jsdata)

        # I think they inserted this to annoy scrapers. :D
        sanatized = sanatized.replace('" + "', '')

        # Remove one more comment
        sanatized = sanatized.replace(
            "// xxx: note - don't internationalize this variable", '')

        return json.loads('{' + sanatized)

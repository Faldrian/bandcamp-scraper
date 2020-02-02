import json
import scrapy
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
                self.log("Crawling new Album: %s" % album_url)
                yield scrapy.Request(url=album_url,
                                     callback=self.parse_album,
                                     cb_kwargs=dict(album_json=item))
            else:
                self.log("Skipping known Album: %s" % album_url)

        if(more_available and page < 1):
            self.log("More available, loading next page: %d." % (page + 1))
            yield self.create_hub_request(tag, page + 1)
        else:
            self.log("No more available or page limit reached. Last page: %d"
                     % page)


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

        numsongs = len(response.css('#track_table [itemprop="tracks"]'))
        loader.add_value('numsongs', numsongs)
        loader.add_value('album_json', album_json)
        return loader.load_item()

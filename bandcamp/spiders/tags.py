import scrapy
import json
import sqlite3
from bandcamp.items import Album
from scrapy.loader import ItemLoader

class TagSpider(scrapy.Spider):
    name = "tags"
    formatstring = '{"filters":{"format":"all","location":0,"sort":"pop","tags":["%s"]},"page":%d}'

    # Close database connection when spider is closed
    def closed(self, reason):
        self.conn.commit()
        self.conn.close()


    def start_requests(self):
        # First thing: connect to database
        # (can't be done in constructor, because self.settings is set later)
        self.conn = sqlite3.connect(self.settings.get('SQLITE_FILE'))
        self.cur = self.conn.cursor()

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
            self.cur.execute('select count(*) from album where album_url=?', [album_url])
            num_rows = self.cur.fetchone()[0]

            if(num_rows == 0):
                self.log("Crawling new Album: %s" % album_url)
                yield scrapy.Request(url=album_url, callback=self.parse_album)
            else:
                self.log("Skipping known Album: %s" % album_url)

        if(more_available and page < 2):
            self.log("More available, loading next page: %d." % (page +1))
            yield self.create_hub_request(tag, page +1)
        else:
            self.log("No more available or page limit reached. Last page: %d" % page)


    def create_hub_request(self, tag, page):
        filter = self.formatstring % (tag, page)

        return scrapy.Request(
            url='https://bandcamp.com/api/hub/2/dig_deeper',
            method='POST',
            body=filter,
            callback=self.parse_dig_deeper,
            cb_kwargs=dict(tag=tag, page=page))


    def parse_album(self, response):
        l = ItemLoader(item=Album(), response=response)
        l.add_value('album_url', response.url)
        l.add_css('title', '#name-section [itemprop="name"]::text')
        l.add_css('artist', '#name-section [itemprop="byArtist"] a::text')
        l.add_css('license', '#license')
        l.add_css('license_url', '#license a.cc-icons::attr(href)')

        numsongs = len(response.css('#track_table [itemprop="tracks"]'))
        l.add_value('numsongs', numsongs)
        return l.load_item()

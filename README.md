# Bandcamp-Scraper

This Scrapy project should help to find albums with creative-commons license.

## Features (implemented)

 - spiders through a music tag until a given number of new CC albums are found
 - stores all crawled albums in a couchdb database
 - includes all track information (length, mp3-url, license per track)

## Setup

1. Install scrapy ( https://docs.scrapy.org/en/latest/intro/install.html )
2. Install couchdb ( https://docs.couchdb.org/en/stable/install/index.html )
   (Currently a local database on default port is assumed)
3. Adjust tag to crawl (currently: Edit `bandcamp/spiders/tags.py` and change variable "tag", will be moved to command line argument)
4. Start crawler in base directory: `scrapy crawl tags`

## Setup Frontend

1. Enable CORS in couchdb
2. Start frontend with `ng serve`

## Wishlist

I will implement this...

### Web-Interface for viewing results
Shows all new results in a list view. Maybe include the "featured track" to quickly listen into the album without opening the album page.

You can mark an album as "Done"

You can export a formattet metadata-string for the album, including title, artist and license (so I can use it for shownotes or as reference when giving CC-credits).

Maybe build something quick using angular ... or even a more specialized toolbox which has some more data-view related features.


### Better Configuration
Adjustable:

- which tag to crawl?
- how many new CC-Albums should be found until terminating?

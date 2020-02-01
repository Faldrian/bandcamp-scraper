# Bandcamp-Scraper

This Scrapy project should help to find albums with creative-commons license.

## Features (implemented)

 - spiders through a music tag until a given number of new CC albums are found
 - stores results in a sqlite database (CC and non-CC albums, to make future spidering faster and put less load on bandcamp servers)

## Wishlist

I will implement this...

### Web-Interface for viewing results
Shows all new results in a list view. Maybe include the "featured track" to quickly listen into the album without opening the album page.

You can mark an album as "Done"

You can export a formattet metadata-string for the album, including title, artist and license (so I can use it for shownotes or as reference when giving CC-credits).


### Use a document based database
Currently much of the crawled data is just dropped.
I need to use a document based database to just store the whole JSON-Object when crawling the list of albums.
When crawling the detail page of the album, I will add some fields with the additional data.
When the user marks the album as "Done", it is modified again.


### Investigate individual tracks
Some albums have mixed licenses on their tracks, some are CC and some not.
The crawler should go an additional step and also get the tracks and their licenses and list them in the document.

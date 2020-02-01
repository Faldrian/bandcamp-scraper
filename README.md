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

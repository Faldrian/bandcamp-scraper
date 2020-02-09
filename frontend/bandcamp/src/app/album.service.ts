import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';

import { Albumfilter } from './albumfilter';

@Injectable({
  providedIn: 'root'
})
export class AlbumService {
  urlAll = "http://127.0.0.1:5984/album/_find?include_docs=true"

  constructor(private http: HttpClient) { }

  findAlbums(albumfilter: Albumfilter) {
    // all albums
    return this.http.post(
      this.urlAll,
      this.prepareFilter(albumfilter)
    ).pipe(map(data => {

      // only return docs
      return data['docs'];

    }));
  }

  private prepareFilter(albumfilter: Albumfilter) {
    let filters = {};

    // only CC music
    filters['license'] = {'$gt': 0};

    if(albumfilter.artist)
      filters['album_json.artist'] = {'$regex': '.*' + albumfilter.artist + '.*'};

    if(albumfilter.title)
      filters['album_json.title'] = {'$regex': '.*' + albumfilter.title + '.*'};

    if(albumfilter.tag)
      filters['tags.' + albumfilter.tag] = {'$exists': true};

    return {selector: filters};
  }
}

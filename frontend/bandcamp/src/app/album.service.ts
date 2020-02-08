import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';

import { Albumdata } from './albumdata';

@Injectable({
  providedIn: 'root'
})
export class AlbumService {
  urlAll = "http://127.0.0.1:5984/album/_all_docs?include_docs=true"

  constructor(private http: HttpClient) { }

  findAlbums() {
    // all albums
    return this.http.get(this.urlAll).pipe(map(data => {

      // map every album of the result list to an Albumdata object
      return data['rows'].map((row: any) => {
          return this.parseAlbum(row['doc']);
      });

    }));
  }

  private parseAlbum(doc: any) {
    let album: Albumdata = {
      _id: doc._id,
      _rev: doc._rev,
      album_url: doc.album_url,
      artist: doc.album_json.artist,
      title: doc.album_json.title,
      license: doc.license,
      numsongs: doc.numsongs,
      tags: doc.tags
    }

    return album;
  }
}

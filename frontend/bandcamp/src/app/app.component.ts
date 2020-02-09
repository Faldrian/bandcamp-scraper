import { Component, OnInit } from '@angular/core';
import { AlbumService } from './album.service';
import { Albumfilter } from './albumfilter';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent implements OnInit {
  title = 'bandcamp';
  displayedColumns: string[] = [
    'artist', 'title', 'numsongs', 'license', 'crawltime', 'albumdate'
  ];
  albums: any[];
  selectedAlbum: any = undefined;

  albumfilter: Albumfilter = {
    artist: undefined,
    tag: undefined,
    title: undefined
   };

  constructor(private albumService: AlbumService) { }

  ngOnInit() {


    this.albumService.findAlbums(this.albumfilter).subscribe((data: any[]) => {
      this.albums = data;
    });
  }

  rowClicked(row) {
    this.selectedAlbum = row;
  }
}

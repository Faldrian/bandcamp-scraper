import { Component, OnInit } from '@angular/core';
import { AlbumService } from './album.service';
import { Albumdata } from './albumdata';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent implements OnInit {
  title = 'bandcamp';
  displayedColumns: string[] = ['artist', 'title', 'numsongs', 'license'];
  albums: Albumdata[];

  constructor(private albumService: AlbumService) { }

  ngOnInit() {
    this.albumService.findAlbums().subscribe((data: Albumdata[]) => {
      this.albums = data;
    });
  }
}

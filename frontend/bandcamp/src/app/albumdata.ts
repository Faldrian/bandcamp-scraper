export interface Albumdata {
  _id: string;
  _rev: string;

  album_url: string;
  artist: string;
  title: string;

  tags: Array<string>;

  license: number;

  numsongs: number;

}

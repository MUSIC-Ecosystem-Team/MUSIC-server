[Back to home documentation](home_documentation.md)

# Playlists endpoints

<br>

# GET /create-playlists

**Method** : `GET`

**Auth required** : YES

**Summary** : Retrieve every playlists of the user.

**Parameters** : None

## Example response

```json
{
    "code": 0,
    "message": "Success",
    "response": [ // List of playlists
        {
            "playlist_id": 1,
            "name": "string",
            "description": "string",
            "musics": [ // List of musics in the playlist with id 1
                {
                    "music_id": 1,
                    "filename": "string",
                    "path": "string",
                    "extension": "string",
                    "album": {
                        "album_id": 1,
                        "name": "string",
                        "artist": {
                            "artist_id": 1,
                            "name": "string",
                            "artist_picture": ""
                        },
                        "date": 2000,
                        "album_picture": "sring",
                        "album_picture_mime": "string"
                    },
                    "artist": {
                        "artist_id": 1,
                        "name": "string",
                        "artist_picture": "string"
                    },
                    "title": "string",
                    "genre": "string",
                    "track_number": "string",
                    "track_total": "string",
                    "disk_number": "string",
                    "disk_total": "string",
                    "date": 2000
                },
                { ... }
            ]
        },
        { ... }
    ]
}
```

<br>

# GET /get-playlist/<playlist_id>

**Method** : `GET`

**Auth required** : YES

**Summary** : Retrieve informations of a playlist.

**Parameters** : None

## Example response

```json
{
    "code": 0,
    "message": "Success",
    "response": {
        "playlist_id": 1,
        "name": "string",
        "description": "string",
        "musics": [ // List of musics in the playlist with id 1
            {
                "music_id": 1,
                "filename": "string",
                "path": "string",
                "extension": "string",
                "album": {
                    "album_id": 1,
                    "name": "string",
                    "artist": {
                        "artist_id": 1,
                        "name": "string",
                        "artist_picture": ""
                    },
                    "date": 2000,
                    "album_picture": "sring",
                    "album_picture_mime": "string"
                },
                "artist": {
                    "artist_id": 1,
                    "name": "string",
                    "artist_picture": "string"
                },
                "title": "string",
                "genre": "string",
                "track_number": "string",
                "track_total": "string",
                "disk_number": "string",
                "disk_total": "string",
                "date": 2000
            },
            { ... }
        ]
    }
}
```

## Example when playlist does not exist

```json
{
    "code": -1,
    "message": "Playlist not found",
    "response": {}
}
```

<br>

# POST /create-playlist

**Method** : `POST`

**Auth required** : YES

**Summary** : Create an empty playlist.

**Parameters** :
- `string` **name** : playlist name
- `string` **description** : playlist description

## Example response

```json
{
    "code": 0,
    "message": "Playlist successfully created",
    "response": {
        "id": 1
    }
}
```

## Example when playlist already exists

```json
{
    "code": -1,
    "message": "A playlist with the same name already exist",
    "response": {}
}
```

<br>

# POST /update-playlist/<playlist_id>

**Method** : `POST`

**Auth required** : YES

**Summary** : Update the playlist referenced by `<playlist_id>`.

**Parameters** :
- `string` **name** : new playlist name
- `string` **description** : new playlist description

## Example response

```json
{
    "code": 0,
    "message": "Playlist successfully updated",
    "response": {}
}
```

## Example when playlist does not exist

```json
{
    "code": -1,
    "message": "The playlist does not exist",
    "response": {}
}
```

<br>

# GET /add-music-to-playlist/<playlist_id>/<music_id>

**Method** : `GET`

**Auth required** : YES

**Summary** : Add the music `<music_id>` to the playlist `<playlist_id>`.

**Parameters** : None

## Example response

```json
{
    "code": 0,
    "message": "Musics successfully added",
    "response": {
        "added": "1/1"
    }
}
```

## Example when Music is already in the playlist

```json
{
    "code": -1,
    "message": "The music is already in the playlist",
    "response": {
        "added": "0/1"
    }
}
```

<br>

# POST /add-musics-to-playlist/<playlist_id>

**Method** : `POST`

**Auth required** : YES

**Summary** : Add the musics in post data to the playlist `<playlist_id>`.

**Parameters** :
- `string` **musics** : music IDs separated by ";" (ex. `"2;23;10;38"`)

## Example response

```json
{
    "code": 0,
    "message": "Musics successfully added",
    "response": {
        "added": "5/5"
    }
}
```

<br>

# GET /remove-playlist/<playlist_id>

**Method** : `GET`

**Auth required** : YES

**Summary** : Remove the playlist `<playlist_id>`.

**Parameters** : None

## Example response

```json
{
    "code": 0,
    "message": "Playlist removed successfully",
    "response": {}
}
```

## Example if the playlist does not exist

```json
{
    "code": -1,
    "message": "The playlist does not exist",
    "response": {}
}
```

<br>

# POST /remove-musics-from-playlist/<playlist_id>

**Method** : `POST`

**Auth required** : YES

**Summary** : Remove the musics in post data from playlist `<playlist_id>`.

**Parameters** :
- `string` **musics** : music IDs separated by ";" (ex. `"2;23;10;38"`)

## Example response

```json
{
    "code": 0,
    "message": "Musics successfully removed",
    "response": {
        "removed": "2/2"
    }
}
```

<br>

[Back to home documentation](home_documentation.md)

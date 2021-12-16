# SERVER API

- [SERVER API](#server-api)
- [Endpoints](#endpoints)
  - [Music request](#music-request)
  - [Music database request](#music-database-request)
  - [Album request](#album-request)
  - [Album database request](#album-database-request)
  - [Artist database request](#artist-database-request)
  - [Artist request](#artist-request)
  - [Artist database request](#artist-database-request-1)
  - [Create user](#create-user)
  - [Get user informations](#get-user-informations)
- [Malformed request](#malformed-request)

<br>

# Endpoints

## Music request

endpoint: /get-music/<id>

method: GET

parameters:
- id: integer

response: a direct link to the music file

```json
{
    "code": "integer",
    "message": "string",
    "response": {
        "album_id": "integer",
        "artistalbum": "string",
        "artist": "string",
        "comment": "string",
        "filename": "string",
        "genre": "string",
        "id": "integer",
        "title": "string",
        "track_number": "integer",
        "year": "integer"
    }
}
```

<br>

## Music database request

endpoint: /get-musics/

method: GET

parameters:
- id: integer

response: a json file

```json
{
    "code": "integer",
    "message": "string",
    "response": [
        {
            "album_id": "integer",
            "artist": "string",
            "comment": "string",
            "filename": "string",
            "genre": "string",
            "id": "integer",
            "title": "string",
            "track_number": "integer",
            "year": "integer"
        },
        {"..."}
    ]
}
```
```
strings can be unicode, o/ kanjis
```

<br>

## Album request

endpoint: /get-album/<id>

method: GET

parameters:
- id: integer

response: a json file

```json
{
    "code": "integer",
    "response": [
        {
            "artist_id": "integer",
            "artist_name": "string",
            "id": "integer",
            "img": "string",
            "name": "string",
            "year": "integer"
        },
        {"..."}
    ]
}
```
```
strings can be unicode, o/ kanjis
```

<br>

<br>

## Album database request

endpoint: /get-albums

method: GET

parameters:
- id: integer

response: a json file

```json
{
    "code": "integer",
    "response": [
        {
            "artist_id": "integer",
            "artist_name": "string",
            "id": "integer",
            "img": "string",
            "name": "string",
            "year": "integer"
        },
        {"..."}
    ]
}
```
```
strings can be unicode, o/ kanjis
```

<br>

<br>

## Artist database request

endpoint: /get-artists

method: GET

parameters:
- id: integer

response: a json file

```json
{
    "code": "integer",
    "artists": [
        {
            "id": "integer",
            "img": "string",
            "name": "string"
        },
        {"..."}
    ]
}
```
```
strings can be unicode, o/ kanjis
```

<br>

## Artist request

endpoint: /get-artist/<id>

method: GET

parameters:
- id: integer

response: a json file

```json
{
    "code": "integer",
    "artists": {
        "id": "integer",
        "img": "string",
        "name": "string"
    }
}
```
```
strings can be unicode, o/ kanjis
```

<br>

## Artist database request

endpoint: /get-artist

method: GET

parameters:
- id: integer

response: a json file

```json
{
    "code": "integer",
    "artists": [
        {
            "id": "integer",
            "img": "string",
            "name": "string"
        },
        {"..."}
    ]
}
```
```
strings can be unicode, o/ kanjis
```

<br>

## Create user

endpoint: /create-user

method: GET

parameters:
- username: string
- password: string

response: a json file

```json
{
    "message": "string",
    "code": "integer"
}
```
```
"code": 0 = success
```

<br>

## Get user informations

endpoint: /get-user-infos

method: GET

parameters:
- username:  "string"

response: a json file

```json
{
    "code": "integer",
    "informations": [
        {
        "id": "integer",
        "library_revision": "integer",
        "creation_date": "string"
        }
    ]
}
```
```
"code": 0 = success
```

<br>

# Malformed request

When a malformed request occur (e.g. parameters missing, POST used instead of GET, ...), a generic error message is sent.

response: a json file

```json
{
    "code": "integer",
    "message": "Bad request"
}
```
```
"code" will never be 0
```

<br>

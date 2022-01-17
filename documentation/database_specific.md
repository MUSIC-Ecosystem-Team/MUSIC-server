[Back to home documentation](home.md)

# Database Specific endpoints

<br>

## GET /database-informations

<hr>

**Method** : `GET`

**Auth required** : NO

**Summary** : Get general database informations such as name and description (can be used to verify if the host is alive).

**Parameters** : Nothing

## Example response
<hr>

```json
{
    "code": 0,
    "message": "Success",
    "response": {
        "name": "string",
        "description": "string"
    }
}
```

<br>

## POST /update-database-informations

<hr>

**Method** : `POST`

**Auth required** : YES

**Summary** : Update general database informations.

**Parameters** :
- `string` **name**: the new name of the database
- `string` **description**: the new description of the database

## Example response on success
<hr>

```json
{
    "code": 0,
    "message": "Database informations updated successfully",
    "response": {}
}
```

<br>

[Back to home documentation](home.md)

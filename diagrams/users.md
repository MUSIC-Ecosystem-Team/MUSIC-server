[Back to home documentation](home_documentation.md)

# Users endpoints

<br>

# POST /register

**Method** : `POST`

**Auth required** : NO

**Summary** : Used to create an account on the server.

**Parameters** :
- `string` **username** : username to register
- `string` **password** : password to use with account

## Example response with user "user" and password "pass"

```json
{
    "code": 0,
    "message": "Accound successfully created",
    "response": {
        "token": "string" // token used for authenticated requests
    }
}
```

## Example when user already exists

```json
{
    "code": -1,
    "message": "Username already exist",
    "response": null
}
```

<br>

# POST /get-token

**Method** : `POST`

**Auth required** : NO

**Summary** : Used to retrieve the token linked to an account.

**Parameters** :
- `string` **username** : username of user
- `string` **password** : password of the account

## Example response with a good user/password combo

```json
{
    "code": 0,
    "message": "Success",
    "response": {
        "token": "string" // token used for authenticated requests
    }
}
```

## Example with a bad user/password combo

```json
{
    "code": -1,
    "message": "Wrong credentials",
    "response": {}
}
```

<br>

# GET /user-infos

**Method** : `GET`

**Auth required** : YES

**Summary** : Used to retrieve the informations linked to an account.

**Parameters** : None

## Example response

```json
{
    "code": 0,
    "message": "Success",
    "response": {
        "user_id": 1,
        "username": "string"
    }
}
```

<br>

# POST /update-profile

`!TODO`

# POST /generate-new-token

`!TODO`

<br>

[Back to home documentation](home_documentation.md)

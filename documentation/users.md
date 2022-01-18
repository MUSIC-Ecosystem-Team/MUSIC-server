[Back to home documentation](home.md)

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

**Method** : `POST`

**Auth required** : YES

**Summary** : Used to retrieve the token linked to an account.

**Parameters** :
- `string` **password** : password of the account (for security reasons)
- `string` **new_username** : new username (can be empty for unchanged)
- `string` **new_password** : new password (can be empty for unchanged)

## Example response with a good password

```json
{
    "code": 0,
    "message": "User updated successfully",
    "response": {}
}
```

# POST /generate-new-token

**Method** : `POST`

**Auth required** : YES

**Summary** : Used to change the user token. The new generated token is sent back in response.

**Parameters** :
- `string` **password** : password of the account (for security reasons)

## Example response

```json
{
    "code": 0,
    "message": "User token updated successfully",
    "response": {
        "token": "string" // Use this new token for requests
    }
}
```

## Example if the password is incorrect:

```json
{
    "code": -1,
    "message": "Password incorrect",
    "response": {}
}
```

<br>

[Back to home documentation](home.md)

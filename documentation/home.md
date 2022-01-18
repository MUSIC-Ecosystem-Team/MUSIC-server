# MUSIC! SERVER Documentation

- [MUSIC! SERVER Documentation](#music-server-documentation)
- [Authentication pipeline](#authentication-pipeline)
- [Make a authenticated request](#make-a-authenticated-request)
- [General error codes](#general-error-codes)
- [Endpoints](#endpoints)

<br>

# Authentication pipeline

The authentication is assured using a unique generated token per account.

Here is a quick diagram who ilustrate how to get your user token:   
![authentication](authentication.png)

<br>

# Make a authenticated request

Once you have your token, there is two way for making a authenticated request:
- By adding `?x-access-token=<token>` on the URL
- By passing `x-access-token` in the header of the request

We only recommand that you use the `second method`, even though the tokens are URL safe, it is a better practice to have your token passed in the header for every requests.

You can check if your authenticated request work by making a request to `/user-infos`.

<br>

# General error codes

For every response you get from the server, there is a response code called `code`. If the code is negative, the operation resulted in a error. If the code is equal 0, The operation completed successfully.

![error_codes](error_codes.png)

<br>

# Endpoints

A Postman collection will be available soon to test all of your requests.

- [Database specifics endpoints](database_specific.md)
- [Users endpoints](users.md)
- [Playlists endpoints](playlists.md)


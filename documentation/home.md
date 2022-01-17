# MUSIC! SERVER Documentation

- [MUSIC! SERVER Documentation](#music-server-documentation)
- [Authentication pipeline](#authentication-pipeline)
- [General error codes](#general-error-codes)
- [Endpoints](#endpoints)

<br>

# Authentication pipeline

The authentication is assured using a unique generated token per account.

Here is a quick diagram who ilustrate how to get your user token:   
![authentication](authentication.png)

<br>

# General error codes

For every response you get from the server, there is a response code called `code`. If the code is negative, the operation resulted in a error. If the code is equal 0, The operation completed successfully.

![error_codes](error_codes.png)

<br>

# Endpoints

- [Database specifics endpoints](database_specific.md)
- [Users endpoints](users.md)
- [Playlists endpoints](playlists.md)


from flask import Flask, Response, redirect, url_for, request, send_file, session
from werkzeug.utils import header_property
from flask_session import Session
from werkzeug.utils import secure_filename
import json
from tags import MusicFileHandler
from database import DatabaseHandler
from utils import returnJSON
from flask_cors import CORS
import hashlib

# Normalize file names from uploads
from unicodedata import normalize
from os import path, makedirs

# send music pictures
from io import BytesIO

app = Flask(__name__)
CORS(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = DatabaseHandler("music.db")

"""
Database: implemented

/database-informations GET
/update-database-informations POST {name: new database name, description: new database description}


Database: not implemented

Nothing \o/

"""
@app.route('/database-informations')
def databaseInformations():
   retCode = -1
   retMessage = "Failed to get database informations"

   infos = db.getDatabaseInformations()
   content = {"name": "", "description": ""}
   if not isinstance(infos, type(None)):
      content["name"] = infos[1]
      content["description"] = infos[2]
      retCode = 0
      retMessage = "Success"

   return returnJSON(retCode, retMessage, content)

@app.route('/update-database-informations', methods = ["POST"])
def updateDatabaseInformations():
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion
   retCode = -1
   retMessage = "Missing parameters"

   name = request.form.get("name")
   description = request.form.get("description")
   print(name)
   print(description)

   if isinstance(name, type(None)) or name == "":
      return returnJSON(retCode, retMessage)
   elif isinstance(description, type(None)) and description == "":
      return returnJSON(retCode, retMessage)
   else:
      retCode = 0
      retMessage = "Database informations updated successfully"
      db.setDatabaseInformations(name, description)

   return returnJSON(retCode, retMessage)

"""
Musics: implemented

/get-musics GET
/get-albums GET
/get-artists GET
/get-music/<music_id> GET
/get-album/<album_id> GET
/get-artist/<artist_id> GET
/get-music-picture/<music_id> GET (not recommanded to use, see /get-album-picture instead)
/get-album-picture/<album_id> GET
/get-music-file/<music_id> GET
/upload-music POST {music: music file to upload}


Musics: not implemented

/update-music POST
/update-album POST
/update-artist POST (maybe)
/remove-music/<music_id> POST
/remove-album/<album_id> POST
/remove-artist/<artist_id> POST
"""
@app.route('/get-musics')
def getMusics():
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   response = db.getMusicsForUser(user_id)
   return returnJSON(0, "Success", response)

@app.route('/get-albums')
def getAlbums():
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   response = db.getAlbumsForUser(user_id)
   return returnJSON(0, "Success", response)

@app.route('/get-music/<int:music_id>')
def getMusic(music_id:int):
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   response = db.getMusicForUser(music_id, user_id)
   return returnJSON("0", "Success", response)

@app.route('/get-album/<int:album_id>')
def getAlbum(album_id:int):
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   response = db.getAlbumForUser(album_id, user_id)
   if response == {}:
      retCode = -1
      retMessage = "Album not found"
   else:
      retCode = 0
      retMessage = "Success"
   return returnJSON(retCode, retMessage, response)

@app.route('/get-music-picture/<int:music_id>')
def getMusicPicture(music_id:int):
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   response = db.getMusicForUser(music_id, user_id)
   if response == {}:
      return returnJSON(-1, "Music does not exist")
   else:
      picture = db.getAlbumPictureForUser(response["album_id"], user_id)
      if picture != {} and picture["album_picture"] != None:
         return send_file(
            BytesIO(picture["album_picture"]),
            mimetype=picture["album_picture_mime"],
            as_attachment=False,
            download_name="cover")
      else:
         with open("ressources/music_default.png", "br") as f:
            return send_file(
               BytesIO(f.read()),
               mimetype="image/png",
               as_attachment=False,
               download_name="cover")

@app.route('/get-album-picture/<int:album_id>')
def getAlbumPicture(album_id:int):
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   picture = db.getAlbumPictureForUser(album_id, user_id)
   if picture != {} and picture["album_picture"] != None:
      return send_file(
         BytesIO(picture["album_picture"]),
         mimetype=picture["album_picture_mime"],
         as_attachment=False,
         download_name="cover")
   else:
      with open("ressources/music_default.png", "br") as f:
         return send_file(
            BytesIO(f.read()),
            mimetype="image/png",
            as_attachment=False,
            download_name="cover")

@app.route('/get-music-file/<int:music_id>')
def getMusicFile(music_id:int):
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   response = db.getMusicForUser(music_id, user_id)
   if response == {}:
      return returnJSON(-1, "File does not exist")
   else:
      return send_file(response["path"])

@app.route('/get-artists')
def getArtists():
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   response = db.getArtistsForUser(user_id)
   return returnJSON(0, "Success", response)

@app.route('/get-artist/<int:artist_id>')
def getArtist(artist_id:int):
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   response = db.getArtistForUser(artist_id, user_id)
   if response == {}:
      retCode = -1
      retMessage = "Artist not found"
   else:
      retCode = 0
      retMessage = "Success"
   return returnJSON(retCode, retMessage, response)

@app.route('/upload-music', methods = ["POST"])
def uploadMusic():
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   f = request.files["music"]
   # https://blog.csdn.net/qq_36390239/article/details/98847888 nice
   filename = normalize('NFKD', f.filename).encode('utf-8', ).decode()
   for sep in  path.sep, path.altsep:
      if sep:
         filename = filename.replace(sep, ' ')

   makedirs("downloads", exist_ok=True)
   saving_path = "downloads/" + filename
   f.save(saving_path)

   music = MusicFileHandler(saving_path)

   if not music.OK():
      return returnJSON(-1, "Error getting tags")
   
   db.addMusicToUser(filename, saving_path, user_id)

   return returnJSON(0, "Music saved as \"" + filename + "\"", music.getTags())

"""
Playlists: implemented

/get-playlists GET
/get-playlist/<playlist_id> GET
/create-playlist POST {name: playlist name, description: playlist description}
/update-playlist/<playlist_id> POST {name: new playlist name, description: new playlist description}
/add-musics-to-playlist/<playlist_id> POST {musics: music IDs separated by ";" (ex. "2;23;10;38")}
/add-music-to-playlist/<playlist_id>/<music_id> GET
/remove-playlist/<playlist_id> GET
/remove-music-from-playlist/<playlist_id>/<music_id> GET
/remove-musics-from-playlist/<playlist_id> POST {musics: music IDs separated by ";" (ex. "2;23;10;38")}


Playlists: not implemented

nothing \o/

"""

@app.route('/get-playlists')
def getPlaylists():
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   response = db.getPlaylistsForUser(user_id)
   return returnJSON(0, "Success", response)

@app.route('/get-playlist/<int:playlist_id>')
def getPlaylist(playlist_id:int):
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   response = db.getPlaylistForUser(playlist_id, user_id)
   if response == {}:
      retCode = -1
      retMessage = "Playlist not found"
   else:
      retCode = 0
      retMessage = "Success"
   return returnJSON(retCode, retMessage, response)

@app.route('/create-playlist', methods = ['POST'])
def CreatePlaylist():
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   retMessage = "Failed to create playlist"
   name = request.form.get("name")
   description = request.form.get("description")

   if name == None or description == None:
      return returnJSON(-1, "Missing parameters")

   retCode, retMessage, id = db.createPlaylistForUser(name, description, user_id)
   return returnJSON(retCode, retMessage, id)

@app.route('/update-playlist/<int:playlist_id>', methods = ['POST'])
def UpdatePlaylist(playlist_id:int):
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   retMessage = "Failed to update playlist"
   name = request.form.get("name")
   description = request.form.get("description")

   if name == None or description == None:
      return returnJSON(-1, "Missing parameters")

   if name == "":
      return returnJSON(-1, "Playlist name can't be empty")

   retCode, retMessage = db.updatePlaylistForUser(playlist_id, name, description, user_id)

   return returnJSON(retCode, retMessage, {})

@app.route('/add-musics-to-playlist/<int:playlist_id>', methods = ['POST'])
def AddMusicsToPlaylist(playlist_id:int):
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   retMessage = "Failed adding musics to playlist"
   musics = request.form.get("musics")

   if musics == None or musics == "":
      return returnJSON(-1, "Missing parameters")

   musics = musics.split(";")

   retCode, retMessage, added = db.addMusicsToPlaylistForUser(playlist_id, musics, user_id)

   return returnJSON(retCode, retMessage, added)

@app.route('/add-music-to-playlist/<int:playlist_id>/<int:music_id>')
def AddMusicToPlaylist(playlist_id:int, music_id:int):
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   retCode, retMessage, added = db.addMusicToPlaylistForUser(playlist_id, music_id, user_id)

   return returnJSON(retCode, retMessage, added)

@app.route('/remove-playlist/<int:playlist_id>')
def RemovePlaylist(playlist_id:int):
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   retCode, retMessage = db.removePlaylistForUser(playlist_id, user_id)

   return returnJSON(retCode, retMessage)

@app.route('/remove-musics-from-playlist/<int:playlist_id>', methods = ['POST'])
def RemoveMusicsFromPlaylist(playlist_id:int):
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   retMessage = "Failed removing musics to playlist"
   musics = request.form.get("musics")

   if musics == None or musics == "":
      return returnJSON(-1, "Missing parameters")

   musics = musics.split(";")

   retCode, retMessage, added = db.removeMusicsFromPlaylistForUser(playlist_id, musics, user_id)

   return returnJSON(retCode, retMessage, added)

@app.route('/remove-music-from-playlist/<int:playlist_id>/<int:music_id>')
def RemoveMusicFromPlaylist(playlist_id:int, music_id:int):
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   retCode, retMessage = db.removeMusicFromPlaylistForUser(playlist_id, music_id, user_id)

   return returnJSON(retCode, retMessage)

"""
Users: implemented

/register POST {username: username to register, password: password}
/get-token POST {username: username of user, password: password of user}
/user-infos GET
/update-profile POST {password: for security reason, new_username: can be empty, new_password: can be empty}
/generate-new-token POST {password: for security reason}


Users: not implemented

Nothing \o/
"""

@app.route('/register', methods = ['POST'])
def register():
   retCode = -1
   retMessage = "Failed to create user"
   c = request.json
   if not request.is_json:
      return returnJSON(-1, "Please send a json")

   if "username" not in c or "password" not in c:
      return returnJSON(-1, "Missing parameters")

   retCode, retMessage, token = db.createUser(c["username"], c["password"])
   return returnJSON(retCode, retMessage, token)

@app.route('/get-token', methods = ['POST'])
def getToken():
   retCode = -1
   retMessage = "Failed to create user"
   username = request.form.get("username")
   password = request.form.get("password")

   if username == None or password == None:
      return returnJSON(-1, "Missing parameters")

   retCode, retMessage, token = db.getUserToken(username, password)
   return returnJSON(retCode, retMessage, token)

@app.route('/user-infos')
def userInfos():
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   response = {"user_id": user_id, "username": username}
   retCode = 0
   retMessage = "Success"
   
   return returnJSON(retCode, retMessage, response)

@app.route('/update-profile', methods = ['POST'])
def updateProfile():
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   password_hash = request.form.get("password")
   newUsername = request.form.get("new_username")
   newPassword = request.form.get("new_password")

   # Check if password field is set
   if password_hash != None:
      password_hash = hashlib.sha512(password_hash.encode()).hexdigest()
   else:
      return returnJSON(0, "Password incorrect")

   if (newUsername == None or newUsername == "") and (newPassword == None or newPassword == ""):
      return returnJSON(0, "Nothing to change")

   user = db.checkUserCredentials(username, password_hash)
   if len(user) < 1:
      return returnJSON(-1, "Password incorrect")

   if newPassword != None:
      newPassword = hashlib.sha512(newPassword.encode()).hexdigest()

   # We can start updating the profile now
   retCode, retMessage = db.changeUserInfos(newUsername, newPassword, user_id)

   return returnJSON(retCode, retMessage)

@app.route('/generate-new-token', methods = ['POST'])
def generateNewToken():
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if retCode == -1:
      return returnJSON(retCode, retMessage)
   # Check connexion

   password = request.form.get("password")

   # Check if password field is set
   if password != None:
      password = hashlib.sha512(password.encode()).hexdigest()
   else:
      return returnJSON(0, "Password incorrect")

   user = db.checkUserCredentials(username, password)
   if len(user) < 1:
      return returnJSON(-1, "Password incorrect")

   # We can start changing the token now
   retCode, retMessage, token = db.changeUserToken(user_id)

   return returnJSON(retCode, retMessage, {'token': token})

""" Check authentication """

def checkAuth():
   token = request.headers.get('x-access-token')
   tokenGet = request.args.get("x-access-token")

   if not isinstance(token, type(None)) and token != "":
      pass
   elif not isinstance(tokenGet, type(None)) and tokenGet != "":
      token = tokenGet
   else:
      return -1, 0, ""
   
   user = db.checkToken(token)
   if len(user) > 0:
      return True, user[0][0], user[0][1]

   return -1, 0, ""

""" 404 page handler """

@app.errorhandler(404)
def page_not_found(error):
   return {"code": -404, "message": "This endpoint does not exist."}, 404

if __name__ == '__main__':
   app.debug = True
   app.run("0.0.0.0", 80)

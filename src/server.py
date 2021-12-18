from flask import Flask, Response, redirect, url_for, request, send_file, session
from werkzeug.utils import header_property
from flask_session import Session
from werkzeug.utils import secure_filename
import json
from tags import MusicFileHandler
from database import DatabaseHandler
from utils import returnJSON
from flask_cors import CORS

# Normalize file names from uploads
from unicodedata import normalize
from os import path

# send music pictures
from io import BytesIO

app = Flask(__name__)
CORS(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = DatabaseHandler("music.db")   

@app.route('/database-informations')
def database_informations():
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

"""
Musics


/get-musics GET
/get-music/<id> GET
/get-music-file/<id> GET

/get-artists GET
/get-artist/<id> GET

/get-albums GET
/get-album/<id> GET

/get-playlists GET
/get-playlist/<id> GET


/create-playlist POST

/upload-music POST
"""
@app.route('/get-musics')
def getMusics():
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if not retCode:
      return returnJSON(retCode, retMessage)
   # Check connexion

   response = db.getMusicsForUser(user_id)
   return returnJSON("0", "Success", response)

@app.route('/get-music/<int:music_id>')
def getMusic(music_id:int):
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if not retCode:
      return returnJSON(retCode, retMessage)
   # Check connexion

   response = db.getMusicForUser(music_id, user_id)
   return returnJSON("0", "Success", response)

@app.route('/get-music-picture/<int:music_id>')
def getMusicPicture(music_id:int):
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if not retCode:
      return returnJSON(retCode, retMessage)
   # Check connexion

   response = db.getMusicForUser(music_id, user_id)
   if response == {}:
      return returnJSON(-1, "Music does not exist")
   else:
      album = db.getAlbum(response["album_id"], user_id)
      return send_file(
         BytesIO(album[0][5]),
         mimetype=album[0][6],
         as_attachment=False,
         download_name="cover")

@app.route('/get-music-file/<int:music_id>')
def getMusicFile(music_id:int):
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if not retCode:
      return returnJSON(retCode, retMessage)
   # Check connexion

   response = db.getMusicForUser(music_id, user_id)
   if response == {}:
      return returnJSON(-1, "File does not exist")
   else:
      return send_file(response["path"])

@app.route('/get-artists')
def getArtists(id:int):
   return ""

@app.route('/get-artist/<int:id>')
def getArtist(id:int):
   return ""

@app.route('/upload-music', methods = ["POST"])
def uploadMusic():
   # Check connexion
   retCode = -1
   retMessage = "Wrong token or x-access-token header not set"
   retCode, user_id, username = checkAuth()
   if not retCode:
      return returnJSON(retCode, retMessage)
   # Check connexion

   f = request.files["music"]
   # https://blog.csdn.net/qq_36390239/article/details/98847888 nice
   filename = normalize('NFKD', f.filename).encode('utf-8', ).decode()
   for sep in  path.sep, path.altsep:
      if sep:
         filename = filename.replace(sep, ' ')

   saving_path = "downloads/" + filename
   f.save(saving_path)

   music = MusicFileHandler(saving_path)

   if not music.OK():
      return returnJSON(-1, "Error getting tags")
   
   db.addMusicToUser(filename, saving_path, user_id)

   return returnJSON("0", "Music saved as \"" + filename + "\"", music.getTags())

"""
Session

/register POST
/get-token POST
/logout GET
/user-infos GET
"""

@app.route('/register', methods = ['POST'])
def register():
   retCode = -1
   retMessage = "Failed to create user"
   username = request.form.get("username")
   password = request.form.get("password")

   if username == None or password == None:
      return returnJSON(-1, "Missing parameters")

   retCode, retMessage = db.createUser(username, password)
   return returnJSON(retCode, retMessage)

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
   if not retCode:
      return returnJSON(retCode, retMessage)
   # Check connexion

   response = {"user_id": user_id, "username": username}
   retCode = 0
   retMessage = "Success"
   
   return returnJSON(retCode, retMessage, response)




@app.route('/test-music')
def test_tags():
   music = MusicFileHandler("musics/02. Von Kaiser - Wavelengths.flac")

   if not music.OK():
      return returnJSON(-1, "Error getting tags")

   return returnJSON(0, "Success", music.getTags())


def checkAuth():
   token = request.headers.get('x-access-token')
   tokenGet = request.args.get("x-access-token")

   if not isinstance(token, type(None)) and token != "":
      pass
   elif not isinstance(tokenGet, type(None)) and tokenGet != "":
      token = tokenGet
   else:
      return False, 0, ""
   
   user = db.checkToken(token)
   if len(user) > 0:
      return True, user[0][0], user[0][1]

   return False, 0, ""

if __name__ == '__main__':
   app.debug = True
   app.run("127.0.0.1", 80)

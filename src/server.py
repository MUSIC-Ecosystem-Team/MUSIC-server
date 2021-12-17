from flask import Flask, Response, redirect, url_for, request, send_file, session
from werkzeug.utils import header_property
from flask_session import Session
from werkzeug.utils import secure_filename
import json
from tags import MusicFileHandler
from database import DatabaseHandler
from utils import returnJSON

# Normalize file names from uploads
from unicodedata import normalize
from os import path

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = DatabaseHandler("music.db")

@app.route('/set/<name>')
def base(name):
   session["name"] = name
   
   return "Something strange.. "

@app.route('/')
def base_redirect():
   if not session.get("name"):
      return "hey"
   else:
      return session.get("name")
   

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

@app.route('/test-send')
def test_send():
   return send_file("musics/04 Just a Dream.mp3")


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
   return ""

@app.route('/get-music/<int:id>')
def getMusic(id:int):
   return ""

@app.route('/get-music-file/<int:id>')
def getMusicFile(id:int):
   return ""

@app.route('/get-artists')
def getArtists(id:int):
   return ""

@app.route('/get-artist/<int:id>')
def getArtist(id:int):
   return ""

@app.route('/upload-music', methods = ["POST"])
def uploadMusic():
   f = request.files["music"]
   # https://blog.csdn.net/qq_36390239/article/details/98847888 nice
   filename = normalize('NFKD', f.filename).encode('utf-8', ).decode()
   for sep in  path.sep, path.altsep:
      if sep:
         filename = filename.replace(sep, ' ')

   f.save("downloads/" + filename)

   music = MusicFileHandler("downloads/" + filename)

   if not music.OK():
      return returnJSON(-1, "Error getting tags")

   return returnJSON("0", "Music saved as \"" + filename + "\"", music.getTags())

"""
Session

/login POST
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

@app.route('/login', methods = ['POST'])
def login():
   retCode = -1
   retMessage = "Missing token"
   token = request.form.get("token")

   if token == None:
      return returnJSON(retCode, retMessage)

   rowCheck = db.checkToken(token)
   if len(rowCheck) < 1:
      retCode = -1
      retMessage = "Wrong token"
      return returnJSON(retCode, retMessage)

   retCode = 0
   retMessage = "Success"
   session["user_id"] = rowCheck[0][0]
   session["username"] = rowCheck[0][1]
   username = {"user_id": session["user_id"], "username": session["username"]}
   
   return returnJSON(retCode, retMessage, username)

@app.route('/logout')
def logout():
   retCode = -1
   retMessage = "No active session"

   if session.get("user_id") == None or session.get("username") == None:
      return returnJSON(retCode, retMessage)

   session["user_id"] = None
   session["username"] = None
   retCode = 0
   retMessage = "Success"
   
   return returnJSON(retCode, retMessage)

@app.route('/user-infos')
def userInfos():
   retCode = -1
   retMessage = "No active session"

   if session.get("user_id") == None or session.get("username") == None:
      return returnJSON(retCode, retMessage)

   response = {"user_id": session["user_id"], "username": session["username"]}
   retCode = 0
   retMessage = "Success"
   
   return returnJSON(retCode, retMessage, response)




@app.route('/test-music')
def test_tags():
   music = MusicFileHandler("musics/04 Just a Dream.mp3")

   if not music.OK():
      return returnJSON(-1, "Error getting tags")

   return returnJSON(0, "Success", music.getTags())




if __name__ == '__main__':
   app.debug = True
   app.run("127.0.0.1", 80)

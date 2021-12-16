from types import NoneType
from flask import Flask, Response, redirect, url_for, request
import json
from tags import MusicFileHandler
from database import DatabaseHandler
from utils import returnJSON

app = Flask(__name__)
db = DatabaseHandler("music.db")

@app.route('/<name>')
def base(name):
   return "Something strange.. " + name

@app.route('/')
def base_redirect():
   return redirect(url_for('base', name = "Sample"))

@app.route('/database-informations')
def database_informations():
   retCode = -1
   retMessage = "Failed to get database informations"

   infos = db.getDatabaseInformations()
   content = {"name": "", "description": ""}
   if not isinstance(infos, NoneType):
      content["name"] = infos[1]
      content["description"] = infos[2]
      retCode = 0
      retMessage = "Success"

   return returnJSON(retCode, retMessage, content)

@app.route('/test-music')
def test_tags():
   music = MusicFileHandler("test-files/04 Just a Dream.mp3")

   if not music.OK():
      exit(1)

   return returnJSON(0, "Success", music.getTags())

if __name__ == '__main__':
   app.debug = True
   app.run("127.0.0.1", 80)

import sqlite3
import hashlib
import secrets
import time

class DatabaseHandler:
    def __init__(self, dbPath):
        try:
            self.con = sqlite3.connect(dbPath, check_same_thread=False)

            self.initDB()

            if self.getDatabaseInformations() == None:
                dbHelper.setDatabaseInformations("Music! Database", "Those informations have been fetched from the sqlite database!")

            dbHelper.setDatabaseInformations("Music! Database", "Those informations have been fetched from the sqlite database!")

            self.OK = True
        except:
            self.OK = False

    def OK(self):
        return self.OK

    def initDB(self):

        cursorObj = self.con.cursor()

        cursorObj.execute("CREATE TABLE IF NOT EXISTS database_informations(\
            id integer PRIMARY KEY AUTOINCREMENT,\
            name text,\
            description text\
        )")

        cursorObj.execute("CREATE TABLE IF NOT EXISTS musics(\
            id              integer PRIMARY KEY AUTOINCREMENT,\
            filename        text,\
            path            text,\
            extension       text,\
            user_id         integer,\
            album_id        integer,\
            genre           text,\
            track_number    integer,\
            track_total     integer,\
            disc_number     integer,\
            disc_total      integer,\
            comment         text,\
            title           text,\
            artist          text,\
            music_year      integer\
        )")

        cursorObj.execute("CREATE TABLE IF NOT EXISTS users(\
            id              integer PRIMARY KEY AUTOINCREMENT,\
            username        text NOT NULL UNIQUE,\
            password_hash   text NOT NULL,\
            token           text NOT NULL,\
            library_revision integer,\
            creation_date   timestamp\
        )")

        cursorObj.execute("CREATE TABLE IF NOT EXISTS artists(\
            id              integer PRIMARY KEY AUTOINCREMENT,\
            name            text,\
            user_id         integer,\
            artist_image    blob\
        )")

        cursorObj.execute("CREATE TABLE IF NOT EXISTS albums(\
            id              integer PRIMARY KEY AUTOINCREMENT,\
            name            text,\
            user_id         integer,\
            artist_id       integer,\
            album_year      integer,\
            cover_image     blob\
        )")

        cursorObj.execute("CREATE TABLE IF NOT EXISTS playlists(\
            id              integer PRIMARY KEY AUTOINCREMENT,\
            name            text,\
            user_id         integer,\
        )")

        cursorObj.execute("CREATE TABLE IF NOT EXISTS musics_playlist(\
            id              integer PRIMARY KEY AUTOINCREMENT,\
            playlist_id            integer,\
            music_id            integer,\
        )")

        self.con.commit()

    def getDatabaseInformations(self):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM database_informations LIMIT 1")

        row = cursorObj.fetchall()
        if row.__len__() < 1:
            return None
        else:
            return row[0]

    def checkUserCredentials(self, username, password_hash):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM users WHERE username = ? AND password_hash = ? LIMIT 1", (username, password_hash))

        row = cursorObj.fetchall()
        return row

    def getUser(self, username):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM users WHERE username = ? LIMIT 1", (username, ))

        row = cursorObj.fetchall()
        return row

    def checkToken(self, token):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM users WHERE token = ? LIMIT 1", (token, ))

        row = cursorObj.fetchall()
        return row

    def getUsers(self):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM users")

        row = cursorObj.fetchall()
        return row

    def createUser(self, username, password):
        if len(self.getUser(username)) > 0:
            return -1, "Username already exist"
        else:
            cursorObj = self.con.cursor()
            cursorObj.execute("INSERT INTO users(username, password_hash, token, library_revision, creation_date) VALUES(?, ?, ?, ?, ?)", (username, hashlib.sha512(password.encode()).hexdigest(), secrets.token_urlsafe(48), 1, time.time()))
            self.con.commit()
            return 0, "Accound successfuly created"
    
    def getUserToken(self, username, password):
        password_hash = hashlib.sha512(password.encode()).hexdigest()
        user = self.checkUserCredentials(username, password_hash)
        if len(user) < 1:
            return -1, "Wrong credentials", {}
        else:
            token = user[0][3]
            return 0, "Success", {"token": token}

    def setDatabaseInformations(self, name, description):
        cursorObj = self.con.cursor()
        cursorObj.execute("UPDATE database_informations SET name = ?, description = ?", (name, description))
        self.con.commit()

    """
    musics function
    """
    def getMusic(self, id):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM musics WHERE id = ?", (id))

        row = cursorObj.fetchall()

        return row
    
    def getMusics(self):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM musics")

        row = cursorObj.fetchall()

        return row


    def getArtist(self, id:int):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM artists WHERE id = ?", id)

        row = cursorObj.fetchall()

        return row
    
    def getArtists(self):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM artists")

        row = cursorObj.fetchall()

        return row


    def getAlbum(self, id:int):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM albums WHERE id = ?", id)

        row = cursorObj.fetchall()

        return row
    
    def getAlbums(self):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM albums")

        row = cursorObj.fetchall()

        return row

    def setMusicInDatabase(self, music):
        sql = "INSERT INTO musics(filename, path, extension, user_id, album_id, genre, track_number, track_total, disc_number, disc_total, comment, title, artist, music_year) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        pass
    
    def setMusics(self, musics):
        for i in musics:
            print(musics[i])
            pass
        sql = ""

dbHelper = DatabaseHandler("music.db")

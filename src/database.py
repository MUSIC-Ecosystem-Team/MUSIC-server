import sqlite3
import hashlib
import secrets
import time
from tags import MusicFileHandler

class DatabaseHandler:
    def __init__(self, dbPath):
        try:
            self.con = sqlite3.connect(dbPath, check_same_thread=False)

            self.initDB()

            if self.getDatabaseInformations() == None:
                self.createDatabaseInformations("Music! Database", "Those informations have been fetched from the sqlite database!")

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
            artist_id       integer,\
            title           text,\
            genre           text,\
            track_number    integer,\
            track_total     integer,\
            disc_number     integer,\
            disc_total      integer,\
            comment         text,\
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
            cover_image     blob,\
            cover_image_mime text\
        )")

        cursorObj.execute("CREATE TABLE IF NOT EXISTS playlists(\
            id              integer PRIMARY KEY AUTOINCREMENT,\
            user_id         integer,\
            name            text,\
            description     text\
        )")

        cursorObj.execute("CREATE TABLE IF NOT EXISTS playlists_musics(\
            id              integer PRIMARY KEY AUTOINCREMENT,\
            playlist_id     integer,\
            music_id        integer\
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

    def createDatabaseInformations(self, name, description):
        cursorObj = self.con.cursor()
        cursorObj.execute("INSERT INTO database_informations(name, description) VALUES(?, ?)", (name, description))
        self.con.commit()
        return 0

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
            return -1, "Username already exist", None
        else:
            cursorObj = self.con.cursor()
            token = secrets.token_urlsafe(48)
            cursorObj.execute("INSERT INTO users(username, password_hash, token, library_revision, creation_date) VALUES(?, ?, ?, ?, ?)", (username, hashlib.sha512(password.encode()).hexdigest(), token, 1, time.time()))
            self.con.commit()
            return 0, "Accound successfuly created", {"token": token}
    
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
    musics functions
    """
    def getMusicForUser(self, music_id, user_id):
        response = {}
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM musics WHERE id = ? AND user_id = ? LIMIT 1", (music_id, user_id))

        row = cursorObj.fetchall()
        if len(row) > 0:
            row = row[0]
            response = {"music_id": row[0], "filename": row[1], "path": row[2], "extension": row[3], "album": self.getAlbumForUser(row[5], user_id), 
                "artist": self.getArtistForUser(row[6], user_id), "title": row[7], "genre": row[8], "track_number": row[9], "track_total": row[10],
                "disk_number": row[11], "disk_total": row[12], "date": row[14]}

        return response
    
    def getMusicsForUser(self, user_id):
        response = []
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM musics WHERE user_id = ?", (user_id, ))

        rows = cursorObj.fetchall()
        if len(rows) > 0:
            for row in rows:
                response.append({"music_id": row[0], "filename": row[1], "path": row[2], "extension": row[3], "album": self.getAlbumForUser(row[5], user_id), 
                "artist": self.getArtistForUser(row[6], user_id), "title": row[7], "genre": row[8], "track_number": row[9], "track_total": row[10],
                "disk_number": row[11], "disk_total": row[12], "date": row[14]})

        return response

    def getArtistForUser(self, artist, user_id):
        response = {}
        cursorObj = self.con.cursor()

        if isinstance(artist, int):
            cursorObj.execute("SELECT * FROM artists WHERE id = ? AND user_id = ?", (artist, user_id))
        elif isinstance(artist, str):
            cursorObj.execute("SELECT * FROM artists WHERE name = ? AND user_id = ?", (artist, user_id))

        row = cursorObj.fetchall()
        if len(row) > 0:
            row = row[0]
            response = {"artist_id": row[0], "name": row[1], "artist_picture": ""}
        else:
            response = {"artist_id": 0, "name": "Various artists", "artist_picture": ""}

        return response
    
    def getAlbumForUser(self, album, user_id, artist_id = None, date = None):
        response = {}
        cursorObj = self.con.cursor()

        if isinstance(album, int):
            cursorObj.execute("SELECT * FROM albums WHERE id = ? AND user_id = ?", (album, user_id))
        elif isinstance(album, str):
            cursorObj.execute("SELECT * FROM albums WHERE name = ? AND artist_id = ? AND user_id = ? AND album_year = ?", (album, artist_id, user_id, date))

        row = cursorObj.fetchall()
        if len(row) > 0:
            row = row[0]
            response = {"album_id": row[0], "name": row[1], "artist": self.getArtistForUser(row[3], user_id), "date": row[4], "album_picture": "/get-album-picture/" + str(row[0]), "album_picture_mime": row[6]}

        return response

    def getAlbumPictureForUser(self, album_id, user_id):
        response = {}
        cursorObj = self.con.cursor()

        cursorObj.execute("SELECT * FROM albums WHERE id = ? AND user_id = ?", (album_id, user_id))

        row = cursorObj.fetchall()
        if len(row) > 0:
            row = row[0]
            response = {"album_picture": row[5], "album_picture_mime": row[6]}

        return response
    
    def getAlbumsForUser(self, user_id):
        response = []
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM albums WHERE user_id = ?", (user_id, ))

        rows = cursorObj.fetchall()
        if len(rows) > 0:
            for row in rows:
                response.append({"album_id": row[0], "name": row[1], "artist": self.getArtistForUser(row[3], user_id), "date": row[4], "album_picture": "", "album_picture_mime": row[6]})

        return response

    def getArtistsForUser(self, user_id):
        response = []
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM artists WHERE user_id = ?", (user_id, ))

        rows = cursorObj.fetchall()
        if len(rows) > 0:
            for row in rows:
                response.append({"artist_id": row[0], "name": row[1], "artist_picture": ""})

        return response

    def getArtistForUser(self, artist, user_id, name = None):
        response = {}
        cursorObj = self.con.cursor()

        if isinstance(artist, int):
            cursorObj.execute("SELECT * FROM artists WHERE id = ? AND user_id = ?", (artist, user_id))
        elif isinstance(artist, str):
            cursorObj.execute("SELECT * FROM artists WHERE name = ? AND user_id = ?", (artist, user_id))

        row = cursorObj.fetchall()
        if len(row) > 0:
            row = row[0]
            response = {"artist_id": row[0], "name": row[1], "artist_picture": ""}

        return response

    def addArtistToUser(self, name, image, user_id):
        if len(name) > 0:
            artist = self.getArtistForUser(name, user_id)
            if artist != {}:
                artistID = artist["artist_id"]
            else:
                cursorObj = self.con.cursor()
                cursorObj.execute("INSERT INTO artists(name, user_id, artist_image) VALUES(?, ?, ?)", (name, user_id, image))
                self.con.commit()
                artist = self.getArtistForUser(name, user_id)
                if artist != {}:
                    artistID = artist["artist_id"]
                else:
                    artistID = 0
        else:
            artistID = 0
        
        return artistID

    def addAlbumToUser(self, name, artist_id, date, image, image_mime, user_id):
        if len(name) > 0:
            album = self.getAlbumForUser(name, user_id, artist_id, date)
            if album != {}:
                albumID = album["album_id"]
            else:
                cursorObj = self.con.cursor()
                cursorObj.execute("INSERT INTO albums(name, user_id, artist_id, album_year, cover_image, cover_image_mime) VALUES(?, ?, ?, ?, ?, ?)", (name, user_id, artist_id, date, image, image_mime))
                self.con.commit()
                album = self.getAlbumForUser(name, user_id, artist_id, date)
                if album != {}:
                    albumID = album["album_id"]
                else:
                    albumID = 0
        else:
            albumID = 0
        
        return albumID

    def addMusicToUser(self, filename, music_path, user_id):
        music = MusicFileHandler(music_path)

        if not music.OK():
            return -1, "Music not found"

        tags = music.getTags()
        picture_mime, picture_data = music.getPicture()

        # Check album artist
        # TODO add checks if album artist don't exist
        albumArtistID = self.addArtistToUser(tags["albumartist"], None, user_id)

        # Check artist
        artistID = self.addArtistToUser(tags["artist"], None, user_id)

        # Check album
        albumID = self.addAlbumToUser(tags["album"], albumArtistID, tags["date"], picture_data, picture_mime, user_id)

        cursorObj = self.con.cursor()
        cursorObj.execute("INSERT INTO musics\
            (filename, path, extension, user_id, album_id, artist_id, title, genre, track_number, track_total, disc_number, disc_total, comment, music_year) \
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (filename, music_path, music.fileType, user_id, albumID, artistID, tags["title"], tags["genre"], tags["tracknumber"], tags["tracktotal"],
            tags["discnumber"], tags["disctotal"], "", tags["date"]))
        self.con.commit()

    def addMusicsToUser(self, musics_path, user_id):
        for music in musics_path:
            self.addMusicToUser(music, user_id)

    """
    playlists functions
    """
    def getPlaylistsForUser(self, user_id):
        response = []
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT id, name, description\
                            FROM playlists\
                            WHERE user_id = ?", (user_id, ))

        rows = cursorObj.fetchall()
        if len(rows) > 0:
            for row in rows:
                response.append({"artist_id": row[0], "name": row[1], "description": row[2]})

        return response

    def getPlaylistForUser(self, playlist_id, user_id):
        response = {}

        # get playlist informations
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT id, name, description\
                            FROM playlists\
                            WHERE id = ? AND user_id = ?", (playlist_id, user_id))

        rows = cursorObj.fetchall()
        if len(rows) > 0:
            for row in rows:
                response = {"playlist_id": row[0], "name": row[1], "description": row[2]}
        else:
            return response

        # get playlist musics
        print(playlist_id)
        print(user_id)
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT pm.music_id\
                            FROM playlists_musics pm\
                            INNER JOIN playlists p on p.id = pm.playlist_id\
                            WHERE pm.playlist_id = ? AND p.user_id = ?", (playlist_id, user_id))

        rows = cursorObj.fetchall()
        if len(row) > 0:
            response["musics"] = []
            for row in rows:
                response["musics"].append(self.getMusicForUser(row[0], user_id))

        return response

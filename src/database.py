import sqlite3
from types import NoneType

class DatabaseHandler:
    def __init__(self, dbPath):
        try:
            self.con = sqlite3.connect(dbPath, check_same_thread=False)

            cursorObj = self.con.cursor()
            cursorObj.execute("CREATE TABLE IF NOT EXISTS database_informations(id integer PRIMARY KEY AUTOINCREMENT, name text, description text)")
            self.con.commit()

            if self.getDatabaseInformations() == NoneType:
                cursorObj.execute("INSERT INTO database_informations(name, description) VALUES('Music! Database', 'Sample description')")
                self.con.commit()

            self.OK = True
        except:
            self.OK = False

    def OK(self):
        return self.OK

    def getDatabaseInformations(self):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM database_informations LIMIT 1")

        row = cursorObj.fetchall()
        if row.__len__() < 1:
            return NoneType
        else:
            return row[0]

    def setDatabaseInformations(self, name, description):
        cursorObj = self.con.cursor()
        # First database
        # Those informations have been fetched from the sqlite database!
        cursorObj.execute("UPDATE database_informations SET name = ?, description = ?", (name, description))
        self.con.commit()

dbHelper = DatabaseHandler("music.db")

dbHelper.setDatabaseInformations("First database", "Those informations have been fetched from the sqlite database!")
print(dbHelper.getDatabaseInformations())



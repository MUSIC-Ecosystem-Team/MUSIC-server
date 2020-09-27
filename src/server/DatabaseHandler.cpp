#include "DatabaseHandler.h"

DatabaseHandler::DatabaseHandler(std::string DatabasePath) {
    char *zErrMsg = NULL;

    if(sqlite3_open(DatabasePath.c_str(), &db)) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        isDatabaseInitialised = false;
    } else {
        fprintf(stderr, "Opened database successfully\n");
        isDatabaseInitialised = true;
    }
}

DatabaseHandler::~DatabaseHandler() {
    sqlite3_close(db);
}

std::vector<std::vector<std::string>> DatabaseHandler::getFilesInDirectory(std::string path) {
    std::vector<std::vector<std::string>> filenames;
    int i = 0;

    for(const auto & entry : std::filesystem::directory_iterator(path)) {
        //std::cout << entry.path() << ", directory: " << entry.is_directory() << std::endl;
        if(entry.is_directory()) {
            std::vector<std::vector<std::string>> filenamesTemp = getFilesInDirectory(entry.path());
            filenames.insert(filenames.end(), filenamesTemp.begin(), filenamesTemp.end());
        } else {
            if((entry.path().extension() == ".mp3") ||
            (entry.path().extension() == ".ogg") ||
            (entry.path().extension() == ".flac")) {

                std::vector<std::string> vectTemp;
                vectTemp.push_back(entry.path());
                std::string filenameTemp = entry.path().filename();
                size_t lastindexTemp = filenameTemp.find_last_of(".");
                vectTemp.push_back(filenameTemp.substr(0, lastindexTemp));
                vectTemp.push_back(entry.path().extension());

                filenames.push_back(vectTemp);
            }
        }
        i += 1;
    }
    return filenames;
}

int DatabaseHandler::createTables() {
    printf("Generating the Music! database...\n");
    
    std::string sql;
    char *zErrMsg = NULL;
    int rc;

    /* CREATE TABLE database_informations */
    sql = "CREATE TABLE database_informations (\
            description         VARCHAR(5000),\
            creation_date        DATETIME\
        )";

    rc = sqlite3_exec(db, sql.c_str(), NULL, 0, &zErrMsg);

    if( rc != SQLITE_OK ){
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    } else {
        //printf("Table database_description created successfully\n");
    }

    /* CREATE TABLE musics */
    sql = "CREATE TABLE musics (\
            id              INTEGER PRIMARY KEY,\
            filename        VARCHAR(5000),\
            path            VARCHAR(5000),\
            extension       VARCHAR(10),\
            album_id        INTEGER,\
            genre           VARCHAR(100),\
            track_number    INTEGER,\
            comment         TEXT(5000),\
            title           VARCHAR(50),\
            artist          VARCHAR(500),\
            year            INTEGER\
        )";

    rc = sqlite3_exec(db, sql.c_str(), NULL, 0, &zErrMsg);

    if( rc != SQLITE_OK ){
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    } else {
        //printf("Table musics created successfully\n");
    }



    /* CREATE TABLE users */
    sql = "CREATE TABLE users (\
            id              INTEGER PRIMARY KEY,\
            username        VARCHAR(250) NOT NULL UNIQUE,\
            password_crypt  VARCHAR(500) NOT NULL,\
            musics_paths    TEXT(10000),\
            paths_size    INTEGER,\
            library_revision    INTEGER,\
            creation_date   DATETIME\
        )";

    rc = sqlite3_exec(db, sql.c_str(), NULL, 0, &zErrMsg);

    if( rc != SQLITE_OK ){
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    } else {
        //printf("Table users created successfully\n");
    }


    /* CREATE TABLE users_musics */
    sql = "CREATE TABLE users_musics (\
            id              INTEGER PRIMARY KEY,\
            user_id         INTEGER,\
            music_id        INTEGER\
        )";

    rc = sqlite3_exec(db, sql.c_str(), NULL, 0, &zErrMsg);

    if( rc != SQLITE_OK ){
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    } else {
        //printf("Table users_musics created successfully\n");
    }


    /* CREATE TABLE albums */
    sql = "CREATE TABLE albums (\
            id              INTEGER PRIMARY KEY,\
            name         VARCHAR(500),\
            artist        VARCHAR(500),\
            cover_image     BLOB\
        )";

    rc = sqlite3_exec(db, sql.c_str(), NULL, 0, &zErrMsg);

    if( rc != SQLITE_OK ){
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    } else {
        //printf("Table albums created successfully\n");
    }

    /* add row to database_informations table */
    sqlite3_stmt *stmt = NULL;
    rc = sqlite3_exec(db, "INSERT INTO database_informations(description, creation_date) VALUES('', DATETIME('now','localtime'))", NULL, 0, &zErrMsg);

    if( rc != SQLITE_OK ){
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    } else {
        //printf("Row inserted successfully\n");
    }

    printf("Done.\n");

    return 0;
}

int DatabaseHandler::initDatabases(std::string path) {
    std::vector<std::vector<std::string>> filenames = getFilesInDirectory(path);

    // print vector of strings
    /* printf("\n      -- ALL FILES --\n");
    for(int i = 0; i < filenames.size(); i++){ 
        printf("%s\n", filenames[i].c_str());
    } */

    TagLib::String fTitle;
    TagLib::String fArtist;
    TagLib::String fAlbum;
    TagLib::String fGenre;
    TagLib::String fComment;
    unsigned int fTrack;
    unsigned int fYear;

    int rc;

    sqlite3_stmt *stmt = NULL;
    rc = sqlite3_prepare_v2(db, "INSERT INTO musics(path, filename, extension, album_id, genre, track_number, comment, title, artist, year) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", -1, &stmt, NULL);

    if(rc != SQLITE_OK) {
        printf("prepare failed: %s\n", sqlite3_errmsg(db));
    } else {

        for(int i = 0; i < filenames.size(); i++){
            

            //get music infos
            TagLib::FileRef f(filenames[i].at(0).c_str());
            fTitle = f.tag()->title();
            fArtist = f.tag()->artist();
            fAlbum = f.tag()->album();
            fGenre = f.tag()->genre();
            fYear = f.tag()->year();
            fComment = f.tag()->comment();
            fTrack = f.tag()->track();


            // get true length of char arrays
            char genre[200];
            strcpy(genre, fGenre.toCString(true));
            int genreLength = sprintf(genre, "%s", genre);

            char comment[200];
            strcpy(comment, fComment.toCString(true));
            int commentLength = sprintf(comment, "%s", comment);

            char title[200];
            strcpy(title, fTitle.toCString(true));
            int titleLength = sprintf(title, "%s", title);

            char artist[200];
            strcpy(artist, fArtist.toCString(true));
            int artistLength = sprintf(artist, "%s", artist);

            sqlite3_bind_text(stmt, 1, filenames[i].at(0).c_str(), filenames[i].at(0).length(), NULL); //path
            sqlite3_bind_text(stmt, 2, filenames[i].at(1).c_str(), filenames[i].at(1).length(), NULL); //filename
            sqlite3_bind_text(stmt, 3, filenames[i].at(2).c_str(), filenames[i].at(2).length(), NULL); //extension
            sqlite3_bind_int(stmt, 4, 1); //TODO, album ID
            sqlite3_bind_text(stmt, 5, genre, genreLength, NULL); //genre
            sqlite3_bind_int(stmt, 6, fTrack);
            sqlite3_bind_text(stmt, 7, comment, commentLength, NULL);
            sqlite3_bind_text(stmt, 8, title, titleLength, NULL);
            sqlite3_bind_text(stmt, 9, artist, artistLength, NULL);
            sqlite3_bind_int(stmt, 10, fYear);
            

            rc = sqlite3_step(stmt);
            if (rc != SQLITE_DONE) {
                printf("execution failed: %s\n", sqlite3_errmsg(db));
            }
            
            
            sqlite3_reset(stmt);
        }
    }


    return 0;
}

bool DatabaseHandler::isDatabaseValid() {
    char *zErrMsg = NULL;
    int returnInt = true;

    if(sqlite3_exec(db, "SELECT * FROM musics", NULL, 0, &zErrMsg) != SQLITE_OK) {
        returnInt = false;
    } else if(sqlite3_exec(db, "SELECT * FROM users", NULL, 0, &zErrMsg) != SQLITE_OK) {
        returnInt = false;
    } else if(sqlite3_exec(db, "SELECT * FROM users_musics", NULL, 0, &zErrMsg) != SQLITE_OK) {
        returnInt = false;
    } else if(sqlite3_exec(db, "SELECT * FROM albums", NULL, 0, &zErrMsg) != SQLITE_OK) {
        returnInt = false;
    } else if(sqlite3_exec(db, "SELECT * FROM database_informations", NULL, 0, &zErrMsg) != SQLITE_OK) {
        returnInt = false;
    }

    if(returnInt == false) {
        printf("Database integrity check failed: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    }

    return returnInt;
}


bool DatabaseHandler::getIsDatabaseInitialised() {
    return isDatabaseInitialised;
}

sqlite3 *DatabaseHandler::getDB() {
    return db;
}

char* DatabaseHandler::serialize(std::vector<std::string> &v, unsigned int *count) {
    unsigned int total_count = 0;

    for(int i = 0; i < v.size(); i++ ) {
        // cout << v[i]<< endl;
        total_count += v[i].length() + 1;
    }

    char *buffer = new char[total_count];

    int idx = 0;

    for(int i = 0; i < v.size(); i++ ) {
        std::string s = v[i];
        for (int j = 0; j < s.size(); j ++ ) {
            buffer[idx ++] = s[j];
        }
        buffer[idx ++] = 0;
    }

    *count  = total_count;

    return buffer;
}

void DatabaseHandler::deserialize(std::vector<std::string> &restore,  char* buffer, int total_count) {
    for(int i = 0; i < total_count; i ++ ) {
        const char *begin = &buffer[i];
        int size = 0;
        while(buffer[i++]) {
            size += 1;
        }
        restore.push_back(std::string(begin, size));
    }
}

bool DatabaseHandler::createUser(std::string username, std::string password, std::string *errMsg) {

    int rc;
    int returnInt = true;

    sqlite3_stmt *stmt = NULL;
    rc = sqlite3_prepare_v2(db, "INSERT INTO users(username, password_crypt, musics_paths, paths_size, library_revision, creation_date) VALUES(?, ?, '', 0, ?, DATETIME('now','localtime'))", -1, &stmt, NULL);

    if(rc != SQLITE_OK) {
        printf("prepare failed: %s\n", sqlite3_errmsg(db));
        *errMsg = sqlite3_errmsg(db);
        returnInt = false;
    } else {

        sqlite3_bind_text(stmt, 1, username.c_str(), username.length(), NULL);
        sqlite3_bind_text(stmt, 2, password.c_str(), password.length(), NULL);

        /* unsigned int total_count = 0;
        char *paths = serialize(musicPath, &total_count);
        sqlite3_bind_text(stmt, 3, paths, total_count, NULL);

        sqlite3_bind_int(stmt, 4, total_count); */ // paths size
        sqlite3_bind_int(stmt, 3, 0); // library revision

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            printf("user creation failed: %s\n", sqlite3_errmsg(db));
            *errMsg = sqlite3_errmsg(db);
            returnInt = false;
        }
    }

    return returnInt;
}

bool DatabaseHandler::updateUserPaths(std::vector<std::string> musicPath, std::string errMsg) {
    return true;
}

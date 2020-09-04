#include <string>
#include <fstream>
#include <filesystem>
#include <string.h>
#include <regex.h>
#include "WebHandler.h"

WebHandler::WebHandler(std::string address, int port, sqlite3 *db) {
    tcpServer = new TcpServer();
    tcpServer->openServer(address, port);
    printf("Server opened\n");

    // init all attributes
    this->db = db;
    lastRequestStatus = LAST_REQUEST_STATUS::NON_INITIALIZED;
    lastRequestEndpoint = "";
    lastRequestType = "";
    lastRequestParams.clear();
    lastRequestHasContentRange = false;
    lastRequestContentRange.first = -1;
    lastRequestContentRange.second = -1;
    lastRequestHasTimedOut = false;
}

WebHandler::~WebHandler() {
    tcpServer->closeServer();
    delete tcpServer;
}

std::string WebHandler::getRequestLine() {
    uint8_t data = 0;
    std::string line = "";
    int timeout = 0, rc = 0;

    while(data != 0x0A && lastRequestHasTimedOut == false)
    {
        rc = tcpServer->getData(&data, 1);

        if(data != 0x0A && rc != -1)
            line += data;

        timeout += 1;
        if(timeout > 10000) {
            lastRequestHasTimedOut = true;
        }
    }

    return line;
}

std::vector<std::string> WebHandler::getRequestHeader() {
    std::vector<std::string> request;
    lastRequestHasTimedOut = false;

    do
    {
        request.push_back(getRequestLine());

        if(lastRequestHasTimedOut)
            break;
        
        /* printf("length: %d\n", request.back().length()); */
        // printf("%s\n", request.back().c_str());
    } while(request.back().length() > 2);
    
    return request;
}

int WebHandler::parseRequest(std::vector<std::string> vectorSource) {
    lastRequestParams.clear();
    lastRequestEndpoint = "";
    lastRequestType = "";
    lastRequestHasContentRange = false;
    lastRequestContentRange.first = -1;
    lastRequestContentRange.second = -1;
    
    regex_t reg;

    // Function call to create regex
    if (regcomp(&reg, "^(GET|OPTIONS)\\s\\/(music|music-db)(\\?.*)\\sHTTP", REG_EXTENDED) != 0) {
        printf("Compilation error.\n");
    }
    
    size_t maxMatches = 10;
    size_t maxGroups = 15;
    regmatch_t groupArray[maxGroups];
    const char *source = vectorSource.at(0).c_str();
    
    if(regexec(&reg, source, maxGroups, groupArray, 0) == 0) {
        unsigned int g = 0;
        for(g = 0; g < maxGroups; g++)
        {
            if(groupArray[g].rm_so == (size_t)-1)
                break; // No more groups

            char sourceCopy[strlen(source) + 1];
            strcpy(sourceCopy, source);
            sourceCopy[groupArray[g].rm_eo] = 0;
            /*printf("Group %u: [%2u-%2u]: %s\n",
                    g, groupArray[g].rm_so, groupArray[g].rm_eo,
                    sourceCopy + groupArray[g].rm_so);*/

        }
        // ALL PARAMS
        char sourceCopy[strlen(source) + 1];
        strcpy(sourceCopy, source);
        sourceCopy[groupArray[3].rm_eo] = 0;
        //printf("param source: %s\n", sourceCopy + groupArray[3].rm_so);

        // ENDPOINT
        char sourceCopy2[strlen(source) + 1];
        strcpy(sourceCopy2, source);
        sourceCopy2[groupArray[2].rm_eo] = 0;
        //printf("endpoint: %s\n", sourceCopy2 + groupArray[2].rm_so);
        const char *endTemp = sourceCopy2 + groupArray[2].rm_so;
        lastRequestEndpoint = endTemp;

        // REQUEST TYPE
        char sourceCopy3[strlen(source) + 1];
        strcpy(sourceCopy3, source);
        sourceCopy3[groupArray[1].rm_eo] = 0;
        //printf("request type: %s\n", sourceCopy3 + groupArray[1].rm_so);
        const char *reqTypeTemp = sourceCopy3 + groupArray[1].rm_so;
        lastRequestType = reqTypeTemp;

        /* IF CONTENT-RANGE */
        for(int i = 0; i < vectorSource.size(); i++)
        {
            std::size_t found = vectorSource[i].find("Range");

            // printf("%s\n", vectorSource[i].c_str());
            if (found!=std::string::npos) {
                printf("%s\n", vectorSource[i].c_str());
                printf("Range in request header.\n");

                // create regex
                if (regcomp(&reg, "=([0-9]+)", REG_EXTENDED) != 0) {
                    printf("Compilation error.\n");
                }

                regmatch_t groupArrayRange[maxGroups];
                unsigned int m;
                const char *sourceRange = vectorSource[i].c_str();
                printf("sourceRange: %s\n", sourceRange);

                if(regexec(&reg, sourceRange, maxGroups, groupArrayRange, 0) == 0) {
                    
                    char sourceCopy[strlen(sourceRange) + 1];
                    strcpy(sourceCopy, sourceRange);
                    sourceCopy[groupArrayRange[1].rm_eo] = 0;
                    // printf("start byte: %lu\n", std::stoi(sourceCopy + groupArrayRange[1].rm_so));
                    lastRequestHasContentRange = true;
                    lastRequestContentRange.first = std::stoi(sourceCopy + groupArrayRange[1].rm_so);
                }



                regfree(&reg);
                
            } else {
                // printf("No Range in request header.\n");
            }
            
        }
        


        /* 2ND PART */

        // create regex
        if (regcomp(&reg, "[?&]+([^=&]+)=([^&]*)", REG_EXTENDED) != 0) {
            printf("Compilation error.\n");
        }

        regmatch_t groupArray2[maxGroups];
        unsigned int m;
        const char *source = sourceCopy + groupArray[3].rm_so;

        regoff_t last_match = 0;
        int Numparams = 0;
        std::string paramName;
        std::string paramValue;
        bool noMoreGroups = false;
        
        while(regexec(&reg, source + last_match, maxGroups, groupArray2, 0) == 0) {
            g = 0;
            Numparams += 1;
            for(g = 0; g < maxGroups; g++)
            {
                if(groupArray2[g].rm_so == (size_t)-1) {
                    noMoreGroups = true;
                    break; // No more groups
                }

                char sourceCopy[strlen(source) + last_match + 1];
                strcpy(sourceCopy, source);
                sourceCopy[groupArray2[g].rm_eo + last_match] = 0;
                if(g == 1) {
                    paramName = sourceCopy + groupArray2[g].rm_so + last_match;
                } else if(g == 2) {
                    paramValue = sourceCopy + groupArray2[g].rm_so + last_match;
                }

                /* printf("Group %u: [%2u-%2u]: %s\n",
                        g, groupArray2[g].rm_so + last_match, groupArray2[g].rm_eo + last_match,
                        sourceCopy + groupArray2[g].rm_so + last_match); */
                
            }
            //printf("\n");
            if(noMoreGroups == true) {
                noMoreGroups = false;
                lastRequestParams.push_back(std::make_pair(paramName, paramValue));
            }

            last_match += groupArray2[0].rm_so + 1;
        }

        if(Numparams == 0) {
            lastRequestStatus = LAST_REQUEST_STATUS::EMPTY;
        } else {
            lastRequestStatus = LAST_REQUEST_STATUS::GOOD;
        }

        regfree(&reg);

    } else {
        lastRequestStatus = LAST_REQUEST_STATUS::BAD;
        return -1;
    }

    regfree(&reg);

    return 0;
}

void WebHandler::handlerLoop() {
    
    while(1)
    {
        tcpServer->connectAClient();
        printf("Client connected\n");

        std::vector<std::string> requestHeader = getRequestHeader();
        if(lastRequestHasTimedOut == false) {
            parseRequest(requestHeader);
            
            printf("%s\n", lastRequestType.c_str());
            if(lastRequestStatus == LAST_REQUEST_STATUS::GOOD)
            {
                if(lastRequestType.compare("GET") == 0)
                {
                    if(lastRequestEndpoint.compare("music") == 0) {
                        printf(" --------------- music request ---------------\n");
                        sendMusicFile();
                    } else if(lastRequestEndpoint.compare("music-db") == 0) {
                        printf(" -------------- music-db request -------------\n");
                        sendMusicDB();
                    } else {
                        printf(" ------------- Forbidden request -------------\n");
                        sendForbiddenResponse();
                    }
                } else if(lastRequestType.compare("OPTIONS") == 0) {
                    printf(" ---------------- OPTIONS request ----------------\n");
                    sendHTTPOptions();
                } else {
                    printf(" -------------- Bad request type -------------\n");
                    sendForbiddenResponse();
                }
                
                
                
            } else {
                printf(" ---------------- bad request ----------------\n");
                sendForbiddenResponse();
            }
        } else {
            printf(" ---------------- Timed out ----------------\n");
        }
        
        
        
        printf("Disconnecting client...\n");
        tcpServer->disconnectAClient();
        printf("Client disconnected\n");
    }
    
}

void WebHandler::sendForbiddenResponse() {
    // header sending
    printf("sending data...");
    std::string header;
    // audio/ogg pour ogg et flac, audio/mpeg pour mp3
    header = "HTTP/1.1 403 Forbidden\r\n";
    header += "\r\n";

    printf("%s\n", "403 Forbidden");
    tcpServer->sendData((void *)header.c_str(), header.length());
}

void WebHandler::sendMusicFile() {
    printf("\n\n");

    std::uintmax_t byteToStartFrom = 0;

    // file choosing
    int choosedID = 0;
    std::string choosedFile;
    std::string choosedFileExt;

    for(int i = 0; i < lastRequestParams.size(); i++)
    {
        if(lastRequestParams[i].first.compare("id") == 0) {
            choosedID = (int) strtol(lastRequestParams[i].second.c_str(), (char **)NULL, 10);
            //choosedID = std::stoi(lastRequestParams[i].second);
            /* printf("param: %s, value: %s\n", lastRequestParams[i].first.c_str(), lastRequestParams[i].second.c_str()); */
            printf("music id: %d\n", choosedID);
            break;
        }
    }
    if(choosedID == 0) {
        printf("Invalid ID, aborting...\n");
        sendForbiddenResponse();
        return;
    } else {
        char select[] = "SELECT * FROM musics WHERE id = ?";
        sqlite3_stmt *stmt;
        if(sqlite3_prepare_v2(db, select, -1, &stmt, NULL) != SQLITE_OK) {
            printf("ERROR: while compiling sql: %s\n", sqlite3_errmsg(db));
            sqlite3_close(db);
            sqlite3_finalize(stmt);

            printf("Error in SQL Prepare, aborting...\n");
            sendForbiddenResponse();
            return;
        }

        bool found = false;

        if(sqlite3_bind_int(stmt, 1, choosedID) != SQLITE_OK) {
            printf("Error in SQL Bind, aborting...\n");
            sendForbiddenResponse();
            return;
        }

        // execute sql statement, and while there are rows returned, print ID
        int ret_code = 0;
        ret_code = sqlite3_step(stmt);
        if(ret_code == SQLITE_ROW) {
            std::string path = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
            choosedFile = path;
            printf("music: %s\n", path.c_str());

            std::string ext = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
            choosedFileExt = ext;
            /* printf("ext: %s\n", ext.c_str()); */
            found = true;
        }

        if(!found) {
            printf("Incorrect ID, aborting...\n");
            sendForbiddenResponse();
            return;
        }

        sqlite3_finalize(stmt);
    }
    

    // Range checking
    if(lastRequestHasContentRange) {
        byteToStartFrom = lastRequestContentRange.first;
    }
    

    // file loading
    std::ifstream myFile;
    myFile.open(choosedFile.c_str(), std::ios_base::out | std::ios_base::app | std::ios_base::binary);
    if(!myFile.is_open())
        return;
    
    // seek to start position
    if(byteToStartFrom > 0)
    {
        myFile.seekg(byteToStartFrom, std::ios::beg);
    }
    

    std::uintmax_t totalFileSize = std::filesystem::file_size(choosedFile.c_str());
    printf("file size : %d\n", totalFileSize);

    // header sending
    /* printf("sending data..."); */
    std::string header;
    // audio/ogg ou audio/flac pour ogg et flac, audio/mpeg pour mp3
    if(lastRequestHasContentRange) {
        header = "HTTP/1.1 206 Partial Content\r\n";
    } else {
        header = "HTTP/1.1 200 OK\r\n";
    }
    
    header += "Cache-Control: no-cache, private\r\n";
    if(choosedFileExt.compare(".flac") == 0)
    {
        header += "Content-Type: audio/flac\r\n";
    } else if(choosedFileExt.compare(".mp3") == 0) {
        header += "Content-Type: audio/mpeg\r\n";
    } else if(choosedFileExt.compare(".ogg") == 0) {
        header += "Content-Type: audio/ogg\r\n";
    }
    
    header += "Accept-Ranges: bytes\r\n";

    if(lastRequestHasContentRange)
    {
        char tempbuffer[150];
        sprintf(tempbuffer, "Content-Range: bytes %lu-%lu/%lu\r\n", byteToStartFrom, totalFileSize - 1, totalFileSize);
        std::string buffsprintf = tempbuffer;
        /* printf("%s\n", tempbuffer); */
        header += buffsprintf;
    }

    header += "Content-Length: ";
    header += std::to_string(totalFileSize - byteToStartFrom);
    header += "\r\n";

    header += "\r\n";

    // printf("%s", header.c_str());
    tcpServer->sendData((void *)header.c_str(), header.length());

    // file sending
    int sizeToRead = 50000;
    char lastBuffer[sizeToRead];
    std::uintmax_t readedSize = byteToStartFrom;
    while(readedSize < totalFileSize)
    {
        if((readedSize + sizeToRead) > totalFileSize) {
            sizeToRead = totalFileSize - readedSize;
        }
        if(!myFile.read(lastBuffer, sizeToRead)) {
            printf("Unable to read the file\n");
            printf("\n\n");
            return;
        }
        
        //printf("readed: %lu\n", readedSize);
        if (tcpServer->sendData((void *)lastBuffer, sizeToRead) == -1) {
            printf("Client closed connection during transfer (%.2fMb/%.2fMb).\n", (float)readedSize / 1000000, (float)totalFileSize / 1000000);
            printf("\n\n");
            return;
        }
        readedSize += sizeToRead;
    }
    myFile.close();
    printf("\n\n");
}

void WebHandler::sendMusicDB() {
    /* printf("\n\n"); */
    // file loading
    std::ifstream myFile;
    myFile.open("tests/db.json", std::ios_base::out | std::ios_base::app | std::ios_base::binary);
    if(!myFile.is_open())
        return;

    std::uintmax_t totalFileSize = std::filesystem::file_size("tests/db.json");
    /* printf("file size : %d\n", totalFileSize); */

    // header sending
    /* printf("sending data...\n"); */
    std::string header;
    // audio/ogg pour ogg et flac, audio/mpeg pour mp3
    header = "HTTP/1.1 200 OK\r\n";
    header += "Access-Control-Allow-Origin: *\r\n";
    header += "Content-Type: application/json\r\n";
    header += "Content-Length: ";
    header += std::to_string(totalFileSize);
    header += "\r\n";
    header += "\r\n";

    // printf("%s", header.c_str());
    tcpServer->sendData((void *)header.c_str(), header.length());
    /* printf("header sent.\n"); */

    // file sending
    int sizeToRead = 50000;
    char lastBuffer[sizeToRead];
    std::uintmax_t readedSize = 0;
    while(readedSize < totalFileSize)
    {
        if((readedSize + sizeToRead) > totalFileSize) {
            sizeToRead = totalFileSize - readedSize;
        }
        if(!myFile.read(lastBuffer, sizeToRead))
            return;
        
        tcpServer->sendData((void *)lastBuffer, sizeToRead);
        readedSize += sizeToRead;
        /* printf("readed size: %lu\n", readedSize);
        printf("total size: %lu\n", totalFileSize); */
    }
    /* printf("\n\n"); */
}

void WebHandler::sendHTTPOptions() {
    /* printf("\n\n"); */
    // header sending
    /* printf("sending data..."); */
    std::string header;

    header = "HTTP/1.1 204 No Content\r\n";
    header += "Allow: OPTIONS, GET\r\n";
    header += "Access-Control-Allow-Origin: *\r\n";
    header += "\r\n";

    printf("%s", header.c_str());
    tcpServer->sendData((void *)header.c_str(), header.length());

    /* printf("\n\n"); */
}
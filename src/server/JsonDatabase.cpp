#include "JsonDatabase.h"

using json = nlohmann::json;
namespace fs = std::filesystem;

JsonDatabase::Database(std::string databaseName)
{

}

JsonDatabase::~Database()
{

}

void JsonDatabase::initDatabase()
{

}

void JsonDatabase::makeDatabaseBakup()
{
    
}

int JsonDatabase::get_databaseContent()
{
    return this->databaseContent;
}

int JsonDatabase::get_dbState()
{
    return this->dbState;
}
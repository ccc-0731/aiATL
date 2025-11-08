import os;
import json;

UPLOAD_FOLDER = '~/database/images'
def saveFile(file, username:str) -> None:
    file.save(os.path.join(UPLOAD_FOLDER, username))

def get_db_as_dict() -> dict:
    """
    gets the database as a dictionary
    :return: the database as a dictionary
    """
    f = open("database/task_list_DB.json", "r")
    data = json.load(f)
    f.close()
    return data

def get_users_as_list() -> list:
    db = get_db_as_dict()
    return list(db)
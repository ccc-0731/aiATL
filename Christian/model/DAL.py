import os;
import json;

UPLOAD_FOLDER = '~/database/images'
def saveFile(file, username:str) -> None:
    file.save(os.path.join(UPLOAD_FOLDER, username))

def eraseUserData(username:str):
    if os.path.exists(os.path.join(UPLOAD_FOLDER, username)):
        os.remove(os.path.join(UPLOAD_FOLDER, username))

def set_sb() -> None:
    """
    sets up the database
    :return: None
    """
    init_db = {
        "jane1": {
        }
    }

    f = open("database/task_list_DB.json", "w")
    json.dump(init_db, f)
    f.close()


def get_db_as_dict() -> dict:
    """
    gets the database as a dictionary
    :return: the database as a dictionary
    """
    f = open("database/userdata.json", "r")
    data = json.load(f)
    f.close()
    return data


def write_to_db(data: dict) -> None:
    """
    writes the data to the database
    :param data: dictionary to write
    :return: None
    """
    f = open("database/task_list_DB.json", "w")
    json.dump(data, f)
    f.close()

def get_users_as_list() -> list:
    db = get_db_as_dict()
    return list(db)


def add_new_user(username: str) -> None:
    db = get_db_as_dict()
    db[username] = {}
    write_to_db(db)

def get_users_as_list() -> list:
    db = get_db_as_dict()
    return list(db)

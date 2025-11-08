UPLOAD_FOLDER = '~/database/images'
import os;
def saveFile(file, username:str) -> None:
    file.save(os.path.join(UPLOAD_FOLDER, username))
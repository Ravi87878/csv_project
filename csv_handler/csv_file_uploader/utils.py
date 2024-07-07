import os
import json
from pathlib import Path

def get_home_path():
    home = str(Path.home())
    return home
def get_work_dir():
    home=get_home_path()
    os.makedirs(home+'/csv', exist_ok=True)
    return home+'/csv'
def create_csv_file_in_dir(name, content, dirs):
    try:
        file_name = name.lower()
        os.makedirs(dirs, exist_ok=True)
        file_path_with_name = os.path.join(dirs, file_name)
        if os.path.isdir(file_path_with_name):
            os.rmdir(file_path_with_name)
        with open(file_path_with_name, 'wb+') as destination:
            for chunk in content.chunks():
                destination.write(chunk)
        return file_name
    except Exception as error:
        print(error)
        return None

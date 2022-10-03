from pathlib import Path
from createdb import create_connection, execute_query, return_path_db

class Directory():
    def __init__(self):
        self.path = 'Not Stated'
        self.create_dir()

    def create_dir(self):
        if return_path_db(create_connection())[0] == self.path:
            self.current_path = self.path
        else:
            self.path = Path.home().joinpath('YaFile')
            if self.path.is_dir() == True:
                self.current_path = self.path
            else:
                Path.mkdir(self.path)
                Path.mkdir(self.path.joinpath('for_users'))
                self.current_path = self.path
                self.states_for_db()

    def states_for_db(self):
        execute_query(create_connection(), f"""
            INSERT INTO
              users_keys (name, value)
            VALUES
              ('path_to_db', '{self.path}')
            """)

    def return_files(self):
        self.files = []
        for child in self.current_path.iterdir():
            self.files.append(child)
        self.child = self.files.copy()
        self.files.clear()
        return self.child

    def choose_fileordir(self, directory):
        self.current_path = self.current_path.joinpath(str(directory))
        return self.current_path

    def return_home(self):
        self.current_path = self.path

    def choose_upload(self, file):
        self.current_path_file = self.current_path.joinpath(file)
        return self.current_path_file

    def is_dir(self):
        return self.current_path.is_dir()

PC = Directory()
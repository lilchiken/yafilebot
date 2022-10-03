from sys import platform
import os
import platform as pl
from createdb import create_connection, execute_query, reading

class Chromedriver():
    def chromedriver_find(self):
        if self.os == 'darwin':
            if self.processor[0] == 'i':
                self.chromedriver = f'{os.getcwd()}/chromedrivers/chromedriver_mac_intel'
            else:
                self.chromedriver = f'{os.getcwd()}/chromedrivers/chromedriver_mac_m1'
        elif self.os == 'linux' or self.os == 'linux2':
            self.chromedriver = f'{os.getcwd()}/chromedrivers/chromedriver_linux'
        elif self.os == 'win32' or self.os == 'cygwin':
            self.chromedriver = f'{os.getcwd()}\chromedrivers\chromedriver_win.exe'
        else:
            self.chromedriver = 'Not Stated'

    def states_for_db(self):
        execute_query(create_connection(),f"""
    INSERT INTO
      users_keys (name, value)
    VALUES
      ('{self.chromedriver}', '100.0.4896.20'),
      ('platform_os', '{self.os}'),
      ('cpu', '{self.processor}')
    """)

    def __init__(self):
        self.os = platform
        if self.os == 'darwin':
            self.processor = pl.processor()
        else:
            self.processor = 'This is row for MacOS :)'
        self.chromedriver_find()
        self.states_for_db()

PC = Chromedriver()

# 100.0.4896.20 - version chromedriver
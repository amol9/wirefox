import os
from os.path import join as joinpath

from redlib.api.system import is_windows


class FirefoxPaths:

    def __init__(self, name='default'):
        self.data_dir = None
        self.get_firefox_dir()


    def get_profile_path(self, name='default'):
        profiles_dir = joinpath(self.data_dir, 'profiles')
        profile = None
        for d in os.listdir(profiles_dir):
            if d.find(name) > -1:
                profile = d
                break
        return joinpath(profiles_dir, profile)


    def get_recovery_js_path(self, profile_name='default'):
        return joinpath(self.get_profile_path(name=profile_name), 'sessionstore-backups', 'recovery.js')


    def get_firefox_dir(self):
        if is_windows():
            self.data_dir = self.get_firefox_dir_windows()
        else:
            return None


    def get_firefox_dir_windows(self):
        appdata = os.environ['APPDATA']
        path = joinpath(appdata, 'mozilla\\firefox')
        return path

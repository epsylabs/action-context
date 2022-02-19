import configparser
from os.path import isfile


class VersionProvider:
    def is_enabled(self):
        return True

    def dump(self, variables):
        current_version = None
        if isfile(".bumpversion.cfg"):
            config = configparser.ConfigParser()
            config.read(".bumpversion.cfg")
            current_version = config["bumpversion"]["current_version"]

        return dict(current_version=current_version)

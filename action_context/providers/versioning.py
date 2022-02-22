import configparser
import os
from os.path import isfile


class VersionProvider:
    def is_enabled(self):
        return True

    def dump(self, variables):
        local = {}

        current_version = ""
        if isfile(".bumpversion.cfg"):
            config = configparser.ConfigParser()
            config.read(".bumpversion.cfg")
            current_version = config["bumpversion"]["current_version"]

        package_version = current_version
        current_version = current_version.split("-")[0]

        local["current_version"] = current_version
        local["package_version"] = package_version
        local["commit_version"] = f"{current_version}-dev{ os.getenv('GITHUB_RUN_ID') }"

        return local

import configparser
import os
from os.path import isfile


class VersionProvider:
    def is_enabled(self):
        return True

    def dump(self, variables):
        local = {}

        current_version = None
        if isfile(".bumpversion.cfg"):
            config = configparser.ConfigParser()
            config.read(".bumpversion.cfg")
            current_version = config["bumpversion"]["current_version"]

        package_version = current_version + "-commit-" + os.getenv("GITHUB_SHA")[0:9]
        if variables.environment == "dev":
            package_version = current_version + "-b${{ github.run_id }}"
        elif variables.environment == "staging":
            package_version = current_version + "-rc${{ github.run_id }}"
        elif variables.environment == "prod":
            package_version = current_version

        local["current_version"] = current_version
        local["package_version"] = package_version

        return local

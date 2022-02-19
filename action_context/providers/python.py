import re
from os.path import isfile

import toml


class PythonProvider:
    def is_enabled(self):
        return True

    def dump(self, variables):
        python_version = "3.8"
        if isfile("pyproject.toml"):
            pyproject = toml.loads(open("pyproject.toml").read())
            python_version = re.sub(
                r"[^\d\\.]", "", pyproject.get("tool").get("poetry").get("dependencies").get("python")
            )

        if isfile(".python-version"):
            python_version = open(".python-version").read().strip()

        return dict(python_version=python_version)

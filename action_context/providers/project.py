import os
import re

from actions_toolkit import core


class ProjectProvider:
    def is_enabled(self):
        return True

    def dump(self, variables):
        local = dict(
            environment=core.get_input("environment"),
            project_id=re.sub(r"\W+", "_", os.getenv("GITHUB_REPOSITORY").split("/")[1])
        )

        return local

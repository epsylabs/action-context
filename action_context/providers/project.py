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

        local["current_deployment_id"] = core.get_input("deployment_id")

        extras = core.get_input("extras")
        if extras:
            for name, value in map(lambda x: x.split("::"), extras.split(",")):
                local[name.strip()] = value.strip()

        return local

import json
import os
from collections import OrderedDict
from os.path import isfile

from actions_toolkit import core
from easydict import EasyDict as edict

from action_context.providers.github import GithubProvider
from action_context.providers.project import ProjectProvider
from action_context.providers.python import PythonProvider
from action_context.providers.versioning import VersionProvider


def get_variables():
    providers = [
        VersionProvider(),
        PythonProvider(),
        GithubProvider(),
        ProjectProvider(),
    ]

    variables = edict(OrderedDict())

    for provider in [p for p in providers if p.is_enabled()]:
        variables.update(provider.dump(variables))

    return variables


def main():
    cache = core.get_input("cache")
    export = core.get_input("export") == "true"
    os.chdir(os.getcwd())

    if cache and isfile(cache):
        core.info(f"Loading cache from: {cache}")
        with open(cache) as f:
            variables = json.load(f)
    else:
        variables = get_variables()
        if cache:
            core.info(f"Dumping cache to: {cache}")
            with open(cache, "w+") as f:
                json.dump(variables, f)

    for k, v in variables.items():
        name = f"project_{k}"
        core.set_output(name, v)
        if export:
            core.export_variable(name, v)


if __name__ == "__main__":
    main()

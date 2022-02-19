import os
from collections import OrderedDict

import click as click
from actions_toolkit import core

from action_context.providers.python import PythonProvider


@click.command()
@click.option("--debug", is_flag=True)
@click.option("--export", is_flag=True, default=False)
@click.option("--save", is_flag=True, default=False)
@click.option("--work-dir", default=os.getcwd())
def main(debug, work_dir, export, save):
    os.chdir(work_dir)
    providers = [
        PythonProvider(),
        # GithubProvider(),
        # AWSProvider(),
    ]

    variables = OrderedDict()

    for provider in [p for p in providers if p.is_enabled()]:
        variables.update(provider.dump(variables))

    for k, v in variables.items():
        core.set_output(k, v)


if __name__ == "__main__":
    main()

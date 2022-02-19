from actions_toolkit import core
from github import Github


class GithubProvider:
    def is_enabled(self):
        return True

    def dump(self, variables):
        g = Github(core.get_input("github_token"))

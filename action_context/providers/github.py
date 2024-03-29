import json
import os

from actions_toolkit import core
from github import Github
from semver import VersionInfo


def previous_release(current_version, versions):
    for version in reversed(versions):
        if version < current_version:
            return version


def get_active_deployment(deployments):
    for deployment in deployments:
        if "success" in list(map(lambda x: x.state, deployment.get_statuses())):
            return deployment


def get_previous_deployment(deployments, current_deployment):
    for deployment in deployments:
        statuses = list(map(lambda x: x.state, deployment.get_statuses()))
        if deployment.id < current_deployment.id and "inactive" in statuses:
            return deployment


class GithubProvider:
    def is_enabled(self):
        return True

    def dump(self, variables):
        g = Github(core.get_input("github_token"))

        local = {}

        repo = g.get_repo(os.getenv("GITHUB_REPOSITORY"))
        releases = repo.get_releases()
        matched_release = next(filter(lambda x: x.tag_name == os.getenv("GITHUB_REF_NAME"), releases), None)

        versions = sorted(map(lambda x: VersionInfo.parse(x.tag_name.strip("v")), releases))

        platform = "unknown"
        topics = repo.get_topics()
        if "aws" in topics:
            platform = "aws"
        elif "android" in topics:
            platform = "android"
        elif "ios" in topics:
            platform = "ios"

        local["platform"] = platform

        current_version = None
        if variables.current_version:
            current_version = VersionInfo.parse(variables.current_version)

        previous_version = previous_release(current_version, versions)
        if previous_version:
            previous_version_tag = next(filter(lambda x: x.tag_name.strip("v") == str(previous_version), releases),
                                        None)
            local["release_previous"] = str(previous_version)
            local["release_previous_tag"] = previous_version_tag.tag_name

        if matched_release:
            local["release_name"] = matched_release.title
            local["release_body"] = matched_release.body
            local["release_body_json"] = json.dumps(matched_release.body)
            local["release_id"] = matched_release.id
            local["release_url"] = matched_release.html_url

        environment = core.get_input("environment")

        if not environment:
            return local

        deployments = repo.get_deployments(environment=environment)
        active_deployment = get_active_deployment(deployments)

        if active_deployment:
            local["active_deployment_id"] = active_deployment.id
            local["active_deployment_sha"] = active_deployment.sha

            previous_deployment = get_previous_deployment(deployments, active_deployment)
            local["previous_deployment_id"] = previous_deployment.id if previous_deployment else None
            local["previous_deployment_sha"] = previous_deployment.sha if previous_deployment else None

        return local

import json

import click
import requests
from prettytable import PrettyTable

GITHUB_USER_INFO = 'https://api.github.com/users/{0}'


@click.command()
@click.argument('username')
@click.option('--repo/--no-repo', default=False, help='List down the repositories if the selected user and url.')
def main(username, repo):
    """Takes a github username as a argument"""
    if username is not None and not repo:
        url = GITHUB_USER_INFO.format(username)
        req = requests.get(url)
        if req is not None and req.content is not None:
            data = json.loads(req.content)
            print_info(data)

    if username is not None and repo:
        table = PrettyTable(['Name', 'forks', 'language', 'open issues'])
        url = GITHUB_USER_INFO.format(username + str("/repos?page=1"))
        recursive_call(url, 1, table)

        if table is not None:
            click.echo(table)


def recursive_call(url, page, table):
    if page != 1:
        location = url.find("=")
        url = url[: location + 1] + str(page)

    req = requests.get(url)
    content = json.loads(req.content)

    if req is not None and content is not None:
        while True:
            if len(content) <= 0:
                return

            for item in content:
                table.add_row([item['name'], item['forks'], item['language'], item['open_issues']])
            page += 1
            recursive_call(url, page, table)


def print_info(data):
    user_info_dict = [{"login": "username"}, "name", "company", "blog", "location", "email", "bio", "followers",
                      "following", {"public_repos": "Repositories"}]
    table = PrettyTable(['Name', 'Value'])

    for info in user_info_dict:
        if type(info) == dict:
            key, display_key = info.items()[0]
            value = data[key]
        else:
            display_key = info
            value = data[info]

        if value is not None and display_key is not None:
            table.add_row([display_key, value])
    click.echo(table)

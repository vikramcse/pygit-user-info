import json

import click
import requests
from prettytable import PrettyTable

GITHUB_USER_INFO = 'https://api.github.com/users/{0}'


@click.command()
@click.option('--username', '-u', help='The github username.')
def main(username):
    if username is not None:
        url = GITHUB_USER_INFO.format(username)
        req = requests.get(url)
        if req is not None and req.content is not None:
            data = json.loads(req.content)
            print_info(data)


def print_info(data):
    user_info_dict = [{"login": "username"}, "name", "company", "blog", "location", "email", "bio", "followers",
                      "following", {"public_repos": "Repositories"}]
    table = PrettyTable(['Name', 'Value'])
    table.padding_width = 10

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

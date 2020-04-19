from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
import requests
import json
import os
from pathlib import Path

base_url = 'https://api.exceltestzone.com.au/api'
base_dir = os.path.dirname(__file__)


def write_to_file(fn, content):
    with open(fn, 'w') as f:
        f.write(content)


def download(username, password, to_folder):

    login_url = '{}/user/login'.format(base_url)
    headers = {'Content-type': "application/json"}

    login_payload = {
        'username': username,
        'password': password
    }

    resp = requests.post(login_url, json=login_payload, headers=headers)

    if resp.status_code == 200:
        resp = resp.json()
        fn = '{}/profile.json'.format(to_folder)
        write_to_file(fn, json.dumps(resp, indent=4))

        # down load testhttps://api.exceltestzone.com.au/api/user/1127/test
        token = resp['token']
        headers['Authorization'] = 'Bearer {}'.format(token)

        child = resp['products'][0]['child']
        child_id = child['id']

        test_url = '{}/user/{}/test'.format(base_url, child_id)
        resp = requests.get(test_url, headers=headers)

        if resp.status_code == 200:
            resp = resp.json()
            tests = resp['success'][0]['test']
            fn = '{}/tests.json'.format(to_folder)

            write_to_file(fn, json.dumps(resp, indent=4))

            for test in tests:
                test_id = test['id']

                question_url = '{}/test/{}/question/'.format(base_url, test_id)

                resp = requests.get(question_url, headers=headers)

                if resp.status_code == 200:
                    fn = '{}/{}.json'.format(to_folder, test_id)
                    write_to_file(fn, json.dumps(resp.json(), indent=4))


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument('--username', required=True,
                            help='Excel test zone username')
        parser.add_argument('--password', required=True, help='Password')

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        current_folder = Path(base_dir)
        to_folder = current_folder.parents[1] / 'static' / 'json'

        username = options['username']
        password = options['password']

        download(username, password, str(to_folder))

        self.stdout.write(self.style.SUCCESS('Database available! '))

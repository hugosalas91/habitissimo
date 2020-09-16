#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import json
import requests


def parse_results(r):
    print('-----')
    print(r.url)
    print('Status: %s' % r.json()['status'])
    print('Msg: %s' % r.json()['msg'])
    print('Results: %s' % json.dumps(r.json()['results'], sort_keys=True, indent=4, separators=(',', ': ')))
    return r.json()['status'], r.json()['msg'], r.json()['results']


class Command(BaseCommand):
    """
    Command in charge of testing the API.
    """
    help = 'Command in charge of testing the API.'

    def handle(self, *args, **options):
        BASE_URL = 'http://web-back:8000/api/sdconnect/'
        token = 'db8b6ac7db6f80a10078b4bt0192e79ea1f679c1'

        headers = {
            'Authorization': 'Token %s' % token,
            'Format': 'application/json',
            'Accept-Language': 'es_ES',
            'charset': 'utf-8'
        }

        # List jobs
        params = {'search':'pint'}
        r = requests.get(BASE_URL + 'jobs/', params=params, headers=headers)
        status, msg, results = parse_results(r)

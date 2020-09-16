__author__ = 'pserra'
import json
import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _

import logging
logger = logging.getLogger(__name__)


class ApiClient(object):
    url = settings.API_URL
    language = 'es'
    token = settings.API_ANONYMOUS_TOKEN
    is_configured = False

    def setup(self, **kwargs):
        self.language = kwargs.get('language', self.language)
        self.token = kwargs.get('token', self.token)

    def call(self, action, path, data=None):
        # type: (object, object, object) -> object
        logger.info("SDC API: %s %s" %(action, path))
        if data:
            token = data.get('token', None)
            if not token:
                token = self.token
        else:
            token = self.token
        if not token:
            token = settings.API_ANONYMOUS_TOKEN

        print(token)

        headers = {
            'Authorization': 'Token %s' % token,
            'Format': 'application/json',
            'Accept-Language': 'es_ES',
            'charset': 'utf-8'
        }

        call_url = self.url + path
        if 'http' in path:
            call_url = path


        if action.upper() == 'POST':
            rq = {}
            rq.update(data)
            headers['Content-Type'] = 'application/json'
            r = requests.post('%s' % call_url,
                              data=json.dumps(rq),
                              headers=headers,
                              verify=False)

        elif action.upper() == 'PUT':
            rq = {}
            rq.update(data)
            headers['Content-Type'] = 'application/json'
            r = requests.put('%s' % call_url,
                              data=json.dumps(rq),
                              headers=headers,
                              verify=False)

        elif action.upper() == 'GET':
            r = requests.get('%s' % call_url,
                             headers=headers,
                             verify=False)

        else:
            r = requests.delete('%s' % call_url,
                             headers=headers,
                             verify=False)

        content_type = r.headers['content-type']
        if int(r.status_code) in [200, 201, 202, 206]:
            r.encoding = 'utf-8'
            if "text/html" in content_type:
                return r
            response = json.loads(r.text.encode('utf-8'))
            return response or {}
        else:
            response = {'status': 0, 'msg': _('Error intentado conectar con el servidor'), 'results': {}}
            if r.status_code != 500:
                r.encoding = 'utf-8'
                response = json.loads(r.text.encode('utf-8'))
            return {'error': response}

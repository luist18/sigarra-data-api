import requests as _requests

from . import utils as _utils

__all__ = ['Session']


class Session:

    def __init__(self, user, password, faculty):
        session = _requests.Session()

        auth_params = {'p_user': user, 'p_pass': password}

        request = session.post(
            _utils.SIGARRA_URLS['homepage'].format(faculty.acronym) + _utils.SIGARRA_URL_HEADERS['auth'], params=auth_params)

        if request.status_code != 200:
            raise ValueError('The authentication parameters are invalid!')

        self.session = session

    def get_html(self, url):
        return self.session.get(url).text

import requests as _requests

from . import utils as _utils

__all__ = ['Session']


class Session:
    """
    A class used to represent a session on SIGARRA.

    Args:
        user            (str): The SIGARRA username
        password        (str): The SIGARRA password
        faculty         (:obj:`Faculty`): The faculty object. The session is created at the SIGARRA web page of the faculty associated to this object

    Attributes:
        session         (:obj:`Session`): The session object created
        
    """

    def __init__(self, user, password, faculty):
        session = _requests.Session()

        auth_params = {'p_user': user, 'p_pass': password}

        request = session.post(
            _utils.SIGARRA_URLS['homepage'].format(faculty.acronym) + _utils.SIGARRA_URL_HEADERS['auth'], params=auth_params)

        if request.status_code != 200:
            raise ValueError('The authentication parameters are invalid!')

        self.session = session

    def get_html(self, url):
        """
        Gets the raw html from a page with the session stored.

        Args:
            url         (str): The URL of the page

        Returns:
            str: The plain html of the page
        """
        
        return self.session.get(url).text

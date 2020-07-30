from bs4 import BeautifulSoup

from . import utils as _utils

__all__ = ['CourseUnit']


class CourseUnit:

    def __init__(self, session, id, name, year, semester):
        self.session = session
        self.id = id
        self.name = name
        self.year = year
        self.semester = semester

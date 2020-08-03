import logging, sys

from . import Session, Course
from . import utils as _utils

__all__ = ['Faculty']


class Faculty:
    """
    A class used to represent a faculty of the University of Porto.

    Args:
        auth            (:obj:`json_object`): A JSON object containing the `user` and the `password` authentication parameters
        acronym         (str): The acronym of the faculty (e.g. FEUP)
        course_ids      (array(int), optional): The ids of the courses

    Attributes:
        name            (str): The name of the faculty (e.g. Faculdade de Engenharia da Universidade do Porto)
        acronym         (str): The acronym of the faculty (e.g. FEUP)
        course_ids      (array(int), optional): The ids of the courses
        courses         (array(:obj:`Course`)): The array of parsed courses
        session         (:obj:`Session`): The session object created with the auth :obj:`json_object`
        verbosity       (bool): Wether the verbosity is enabled or not

    """

    def __init__(self, auth, acronym, course_ids=[], verbosity=False):
        self.acronym = acronym.lower()
        self.name = _utils.FACULTIES[self.acronym]
        self.course_ids = course_ids
        self.courses = []
        self.session = Session(auth['user'], auth['password'], self)
        self.verbosity = verbosity

        #logging.basicConfig(
        #    format='[%(levelname)] %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        #logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

        root = logging.getLogger('sigarra_data_scrapper')
        root.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        handler.setFormatter(formatter)
        root.addHandler(handler)
        
        self.logger = root

    def fetch_courses(self):
        """
        Fetches the faculty courses.

        For each course id in the course_ids array the method fetches the respective :obj:`Course` object.
        """
        for id in self.course_ids:
            if self.verbosity is True:
                self.logger.info('Getting data for course with params: {{ \'id\': {} }}'.format(id))

            self.courses.append(Course(self, id))

    def set_verbose(self, verbosity):
        """
        Sets the verbosity to a given value.
        """
        self.verbosity = verbosity

from . import Session, Course

__all__ = ['Faculty']


class Faculty:
    """
    A class used to represent a faculty of the University of Porto.

    Args:
        auth            (:obj:`json_object`): A JSON object containing the `user` and the `password` authentication parameters
        name            (str): The name of the faculty (e.g. Faculdade de Engenharia da Universidade do Porto)
        acronym         (str): The acronym of the faculty (e.g. FEUP)
        course_ids      (array(int), optional): The ids of the courses

    Attributes:
        name            (str): The name of the faculty (e.g. Faculdade de Engenharia da Universidade do Porto)
        acronym         (str): The acronym of the faculty (e.g. FEUP)
        course_ids      (array(int), optional): The ids of the courses
        courses         (array(:obj:`Course`)): The array of parsed courses
        session         (:obj:`Session`): The session object created with the auth :obj:`json_object`
        
    """

    def __init__(self, auth, name, acronym, course_ids=[]):
        self.name = name
        self.acronym = acronym.lower()
        self.course_ids = course_ids
        self.courses = []
        self.session = Session(auth['user'], auth['password'], self)

    def fetch_courses(self):
        """
        Fetches the faculty courses.

        For each course id in the course_ids array the method fetches the respective :obj:`Course` object.
        """
        for id in self.course_ids:
            self.courses.append(Course(self, id))

from . import Session, Course

__all__ = ['Faculty']


class Faculty:

    def __init__(self, auth, name, acronym, course_ids=[]):
        self.name = name
        self.acronym = acronym.lower()
        self.course_ids = course_ids
        self.courses = []
        self.session = Session(auth['user'], auth['password'], self)

    def fetch_courses(self):
        for id in self.course_ids:
            self.courses.append(Course(self, id))

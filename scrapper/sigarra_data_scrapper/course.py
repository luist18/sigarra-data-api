from bs4 import BeautifulSoup
import json

from . import CourseUnit
from . import utils as _utils

__all__ = ['Course']


class Course:
    """
    A class used to represent a course of any faculty of the University of Porto.

    Args:
        faculty             (:obj:`Faculty`): The faculty object associated to this course
        curricular_plan_id  (int): The curricular plan id of the course. The id of MIEQ is 2708

    Attributes:
        faculty             (:obj:`Faculty`): The faculty object associated to this course
        curricular_plan_id  (int): The curricular plan id of the course. The id of MIEQ is 2708
        name                (str): The name of the course
        course_units        (array(:obj:`CourseUnit`)): The course units of the course
        difficulty          (float): The difficulty of the course based in the data fetched. The difficulty is a float
                            value between 0.0 and 5.0. Lower the value lower the difficulty

    """

    def __init__(self, faculty, curricular_plan_id):
        self.faculty = faculty
        self.curricular_plan_id = curricular_plan_id

        self.html = self.faculty.session.get_html(
            _utils.SIGARRA_URLS['course_plan'].format(self.faculty.acronym, self.curricular_plan_id))

        self.soup = BeautifulSoup(self.html, 'html.parser')

        self.fetch_name()
        self.fetch_course_units()
        self.calculate_difficulty()

    def fetch_name(self):
        """
        Fetches the name of the course.

        This method is responsible for fetching the course name in the course page HTML. The course name is the second `h1`
        in the `conteudoinner` div.
        """

        # The name is the second h1 in the div with the conteudoinner id
        div = self.soup.find('div', {'id': 'conteudoinner'})

        name = div.find_all('h1')[1].text

        if name is None:
            raise ValueError('The course does not have a valid name')

        self.name = name

        if self.faculty.verbosity is True:
            self.faculty.logger.info('Found name: {{ \'name\': {} }}'.format(name))

    def fetch_course_units(self):
        """
        Fetches the course units of the course.
        
        For each year and semester of the course this method fetches each course unit and stores it as a :obj:`CourseUnit`
        in the course units array.
        """
        self.course_units = []

        course_units_raw = _utils.get_course_units(self.soup)

        if self.faculty.verbosity is True:
            self.faculty.logger.info('Found {} years'.format(len(course_units_raw)))

        for year in course_units_raw:
            for semester in course_units_raw[year]:
                for course_unit_raw in course_units_raw[year][semester]:
                    if self.faculty.verbosity is True:
                        self.faculty.logger.info('Getting data for course unit with params: {}'.format(course_unit_raw))

                    c_unit = CourseUnit(self.faculty, course_unit_raw['id'], course_unit_raw['name'], year, semester, course_unit_raw['code'],
                                        course_unit_raw['acronym'], course_unit_raw['credits'])

                    self.course_units.append(c_unit)

    def calculate_difficulty(self):
        """
        Calculates the difficulty rating of the course.

        Based on the average approve rate and grades from 2010 to 2018 the method computes a rating from 0.0 to 5.0 that
        represents the difficulty of each course unit. The lower the value lower the difficulty. The difficulty of the course
        is the average difficulty of all course units.
        """
        count = 0
        sum = 0

        for course_unit in self.course_units:
            if course_unit.difficulty is None:
                continue

            count += 1
            sum += course_unit.difficulty

        if count == 0:
            self.difficulty = None

            if self.faculty.verbosity is True:
                self.faculty.warning.info('Error while finding difficulty')

            return

        self.difficulty = sum / count

    def json_object(self):
        """
        Creates a JSON object with the object data.

        This method transforms the object into a JSON object with every data stored in the class.
        """
        course_units_object = []

        for course_unit in self.course_units:
            course_units_object.append(course_unit.json_object())

        object = {
            'name': self.name,
            'id': self.curricular_plan_id,
            'difficulty': self.difficulty,
            'course_units': course_units_object
        }

        return object

    def to_json(self, filename):
        """
        Exports the JSON object to a file.

        This method exports the JSON object created in the method json_object() to a folder. The filename is specified in the
        arguments.

        Args:
            filename        (str): the filename
        """
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(self.json_object(), outfile,
                      indent=4, ensure_ascii=False)

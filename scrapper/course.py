from bs4 import BeautifulSoup
import json

from . import CourseUnit
from . import utils as _utils

__all__ = ['Course']


class Course:

    def __init__(self, session, curricular_plan_id):
        self.session = session
        self.curricular_plan_id = curricular_plan_id

        self.html = self.session.get_html(
            _utils.SIGARRA_URLS['course_plan'].format(self.curricular_plan_id))

        self.soup = BeautifulSoup(self.html, 'html.parser')

        self.fetch_name()
        self.fetch_course_units()
        self.calculate_difficulty()

    def fetch_name(self):
        # The name is the second h1 in the div with the conteudoinner id
        div = self.soup.find('div', {'id': 'conteudoinner'})

        name = div.find_all('h1')[1].text

        if name is None:
            raise ValueError('The course does not have a valid name')

        self.name = name

    def fetch_course_units(self):
        self.course_units = []

        course_units_raw = _utils.get_course_units(self.soup)

        for year in course_units_raw:
            for semester in course_units_raw[year]:
                for course_unit_raw in course_units_raw[year][semester]:
                    c_unit = CourseUnit(self.session, course_unit_raw['id'], course_unit_raw['name'], year, semester, course_unit_raw['code'],
                                        course_unit_raw['acronym'], course_unit_raw['credits'])

                    self.course_units.append(c_unit)

    def calculate_difficulty(self):
        count = 0
        sum = 0

        for course_unit in self.course_units:
            if course_unit.difficulty is None:
                continue

            count += 1
            sum += course_unit.difficulty

        if count == 0:
            self.difficulty = None
            return

        self.difficulty = sum / count

    def json_object(self):
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
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(self.json_object(), outfile,
                      indent=4, ensure_ascii=False)

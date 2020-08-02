from bs4 import BeautifulSoup

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
        # In the course study plan the tables with the course units are the 3, 4, 7, 8, 11, 12, 15, 16, 19, 20
        # 3, 4 - 1st year
        # 7, 8 - 2nd year
        # 11, 12 - 3rd year
        # 15, 16 - 4th year
        # 19, 20 - 5th year
        self.course_units = []

        tables = self.soup.find_all('table')

        course_unit_tables = []

        course_unit_tables.extend(tables[3:5])
        course_unit_tables.extend(tables[7:9])
        course_unit_tables.extend(tables[11:13])
        course_unit_tables.extend(tables[15:17])
        course_unit_tables.extend(tables[19:21])

        for i in range(0, len(course_unit_tables)):
            year = (int)(i / 2 + 1)
            semester = (int)(i % 2 + 1)

            table = course_unit_tables[i]

            course_units = table.find_all('td', {'class', 't'})

            for course_unit in course_units:
                a = course_unit.find('a')

                if a is None:
                    continue

                href = a.get('href')

                if href is None:
                    continue
                elif 'ucurr_geral' not in href:
                    continue

                id = href.split('=')[1]
                name = a.text

                c_unit = CourseUnit(self.session, id, name, year, semester)

                self.course_units.append(c_unit)

    def calculate_difficulty(self):
        count = 0
        sum = 0

        for course_unit in self.course_units:
            if course_unit.difficulty is None:
                continue

            count += 1
            sum += course_unit.difficulty

        self.difficulty = sum / count

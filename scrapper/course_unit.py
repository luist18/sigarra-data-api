from bs4 import BeautifulSoup

from . import CourseUnitYear
from . import utils as _utils

__all__ = ['CourseUnit']


class CourseUnit:

    def __init__(self, session, id, name, year, semester):
        self.session = session
        self.id = id
        self.name = name
        self.year = year
        self.semester = semester

        self.fetch_years(2010, 2019)
        self.calculate_grades()
        self.calculate_rate()
        # self.calculate_difficulty()

    def fetch_years(self, starting_year, finishing_year):
        self.years = {}

        for year in range(2010, 2019):
            print('Fetching', year, 'data for', self.name)

            course_unit_year = CourseUnitYear(self.session, self.id, year)

            self.years[year] = course_unit_year

    def calculate_grades(self):
        self.grades = {}

        for year_item in self.years.items():
            year = year_item[0]
            grades = year_item[1].grades

            if grades is None:
                continue

            for grade_item in grades.items():
                grade = grade_item[0]
                count = grade_item[1]

                if grade in self.grades:
                    self.grades[grade] += count
                else:
                    self.grades[grade] = count

    def calculate_rate(self):
        sum = 0

        for year_item in self.years.items():
            rate = year_item[1].pass_rate

            if rate is None:
                continue

            sum += rate

        return sum / len(self.years)

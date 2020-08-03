from bs4 import BeautifulSoup

from . import CourseUnitYear
from . import utils as _utils

__all__ = ['CourseUnit']


class CourseUnit:

    def __init__(self, faculty, id, name, year, semester, code, acronym, credits):
        self.faculty = faculty
        self.id = id
        self.name = name
        self.year = year
        self.semester = semester
        self.code = code
        self.acronym = acronym
        self.credits = credits

        print('Getting data for', self.name)

        self.fetch_years(2010, 2019)
        self.calculate_grades()
        self.calculate_average_rate()
        self.calculate_difficulty()

    def fetch_years(self, starting_year, finishing_year):
        self.years = {}

        for year in range(2010, 2019):

            course_unit_year = CourseUnitYear(self.faculty, self.id, year)

            self.years[year] = course_unit_year

    def calculate_grades(self):
        self.grades = {}
        self.grade_count = 0

        for year_item in self.years.items():
            year = year_item[0]
            grades = year_item[1].grades

            if grades is None:
                continue

            for grade_item in grades.items():
                grade = grade_item[0]
                count = grade_item[1]

                self.grade_count += count

                if grade in self.grades:
                    self.grades[grade] += count
                else:
                    self.grades[grade] = count

        self.calculate_average_grade()

    def calculate_average_grade(self):
        average = 0.0

        for key in self.grades:
            prob = self.grades[key] / self.grade_count

            average += prob * key

        self.average_grade = average

    def calculate_average_rate(self):
        sum = 0
        count = 0

        for year_item in self.years.items():
            rate = year_item[1].pass_rate

            if rate is None:
                continue

            sum += rate
            count += 1

        if count == 0:
            self.average_pass_rate = None
            return

        self.average_pass_rate = sum / count

    def calculate_difficulty(self):
        if self.average_grade is None or self.average_pass_rate is None:
            self.difficulty = None
            return

        average_weighted = self.average_grade / 20.0 * 0.60
        pass_rate_weighted = self.average_pass_rate / 100.0 * 0.40

        self.difficulty = (average_weighted + pass_rate_weighted) * 5

    def json_object(self):
        years_object = {}

        for year_item in self.years.items():
            year = year_item[0]
            years_object[year] = year_item[1].json_object()

        object = {
            'id': self.id,
            'name': self.name,
            'year': self.year,
            'semester': self.semester,
            'code': self.code,
            'acronym': self.acronym,
            'credits': self.credits,
            'average_grade': self.average_grade,
            'average_pass_rate': self.average_pass_rate,
            'difficulty': self.difficulty,
            'grade_count': self.grade_count,
            'grades': self.grades,
            'years': years_object
        }

        return object

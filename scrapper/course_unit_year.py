from bs4 import BeautifulSoup
import math

from . import utils as _utils

__all__ = ['CourseUnitYear']


class CourseUnitYear:

    def __init__(self, session, id, year):
        self.session = session
        self.id = id
        self.year = year
        self.grade_count = 0
        self.pass_rate = None
        self.grades = None
        self.average_grade = None

        self.html_rate = self.session.get_html(
            _utils.SIGARRA_URLS['rate_stats'].format(id, year))
        self.html_grades = self.session.get_html(
            _utils.SIGARRA_URLS['grade_stats'].format(id, year))

        self.rate_soup = BeautifulSoup(self.html_rate, 'html.parser')
        self.grades_soup = BeautifulSoup(self.html_grades, 'html.parser')

        self.fetch_pass_rate()
        self.fetch_grades()
        self.calculate_difficulty()

    def fetch_pass_rate(self):
        # The data table is the fourth on the page
        try:
            table = self.rate_soup.find_all('table')[3]

            # The rate is the fifth column in the table
            rate = table.find_all('td', {'class': 'k n'})[4].text

            self.pass_rate = (float)(rate)
        except:
            self.pass_rate = None

    def fetch_grades(self):
        # The grades are the first table with the class dados
        try:
            table = self.grades_soup.find('table', {'class': 'dados'})

            rows = table.find_all('tr', {'class': 'd'})

            self.grades = {}

            for row in rows:
                result = row.find('td', {'class': 'k t'}).text
                count = (int)(row.find('td', {'class': 'n'}).text)

                if 'Reprovado' in result or 'Sem frequência' in result:
                    continue

                grade = (int)(_utils.NUMBERS_PT[result])

                self.grades[grade] = count
                self.grade_count += count

            self.calculate_average_grade()
        except:
            self.grades = None

    def calculate_average_grade(self):
        average = 0.0

        for key in self.grades:
            prob = self.grades[key] / self.grade_count

            average += prob * key

        self.average_grade = average

    def calculate_difficulty(self):
        if self.average_grade is None or self.pass_rate is None:
            self.difficulty = None
            return

        average_weighted = self.average_grade / 20.0 * 0.60
        pass_rate_weighted = self.pass_rate / 100.0 * 0.40

        self.difficulty = (average_weighted + pass_rate_weighted) * 5

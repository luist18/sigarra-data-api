#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import math

from . import utils as _utils

__all__ = ['CourseUnitYear']


class CourseUnitYear:
    """
    A class used to represent a course unit instance taught at of any course from any faculty of the University of Porto.

    Args:
        faculty             (:obj:`Faculty`): The faculty object associated to this course unit instance
        id                  (int): The id of the course unit
        year                (int): The year of the instance

    Attributes:
        faculty             (:obj:`Faculty`): The faculty object associated to this course unit instance
        id                  (int): The id of the course unit
        year                (int): The year of the instance
        grade_count:        (int): The grade count of this course unit instance
        pass_rate:          (float): The pass rate of this course unit instance
        grades:             (dict): The dictionary of grades of this course unit instance
        average_grade:      (float): The average grade of this course unit instance
        difficulty:         (float): The difficulty of the course unit instance based in the data fetched. The difficulty is a float
                            value between 0.0 and 5.0. Lower the value lower the difficulty

    """

    def __init__(self, faculty, id, year):
        self.faculty = faculty
        self.id = id
        self.year = year
        self.grade_count = 0
        self.pass_rate = None
        self.grades = None
        self.average_grade = None

        self.html_rate = self.faculty.session.get_html(
            _utils.SIGARRA_URLS['rate_stats'].format(self.faculty.acronym, id, year))
        self.html_grades = self.faculty.session.get_html(
            _utils.SIGARRA_URLS['grade_stats'].format(self.faculty.acronym, id, year))

        self.rate_soup = BeautifulSoup(self.html_rate, 'html.parser')
        self.grades_soup = BeautifulSoup(self.html_grades, 'html.parser')

        self.fetch_pass_rate()
        self.fetch_grades()
        self.calculate_difficulty()

    def fetch_pass_rate(self):
        """
        Fetches the pass rate for this course unit instance.

        The pass rate is the fifth `td` in the fourth `table` of the html page.
        """

        # The data table is the fourth on the page
        try:
            table = self.rate_soup.find_all('table')[3]

            # The rate is the fifth column in the table
            rate = table.find_all('td', {'class': 'k n'})[4].text

            self.pass_rate = (float)(rate)
        except:
            self.pass_rate = None

    def fetch_grades(self):
        """
        Fetches the grades for this course unit instance.
        """

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
        """
        Calculates the average grade.
        """
        average = 0.0

        for key in self.grades:
            prob = self.grades[key] / self.grade_count

            average += prob * key

        self.average_grade = average

    def calculate_difficulty(self):
        """
        Calculates the difficulty rating of the course unit.

        Based on the average approve rate and grades from 2010 to 2018 the method computes a rating from 0.0 to 5.0 that
        represents the difficulty of each course unit. The lower the value lower the difficulty. The difficulty of the course unit
        is the weighted sum of 60% of the normalized average grade and 40% of the normalized pass rate.
        """
        if self.average_grade is None or self.pass_rate is None:
            self.difficulty = None
            return

        average_weighted = self.average_grade / 20.0 * 0.60
        pass_rate_weighted = self.pass_rate / 100.0 * 0.40

        self.difficulty = (average_weighted + pass_rate_weighted) * 5

    def json_object(self):
        """
        Creates a JSON object with the object data.

        This method transforms the object into a JSON object with every data stored in the class.
        """
        object = {
            'year': self.year,
            'average_grade': self.average_grade,
            'pass_rate': self.pass_rate,
            'difficulty': self.difficulty,
            'grade_count': self.grade_count,
            'grades': self.grades
        }

        return object

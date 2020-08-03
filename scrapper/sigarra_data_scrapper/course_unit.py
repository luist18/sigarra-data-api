from bs4 import BeautifulSoup

from . import CourseUnitYear
from . import utils as _utils

__all__ = ['CourseUnit']


class CourseUnit:
    """
    A class used to represent a course unit taught at of any course from any faculty of the University of Porto.

    Args:
        faculty             (:obj:`Faculty`): The faculty object associated to this course unit
        id                  (int): The id of the course unit
        name                (str): The name of the course unit
        year                (int): The year which the course unit is taught
        semester            (int): The semester which the course unit is taught
        code                (str): The SIGARRA code of the course unit
        acronym             (str): The acronym of the course unit
        credits             (float): The number of the ECTS of the course unit

    Attributes:
        faculty             (:obj:`Faculty`): The faculty object associated to this course unit
        id                  (int): The id of the course unit
        name                (str): The name of the course unit
        year                (int): The year which the course unit is taught
        semester            (int): The semester which the course unit is taught
        code                (str): The SIGARRA code of the course unit
        acronym             (str): The acronym of the course unit
        credits             (float): The number of the ECTS of the course unit
        years               (dict): The years data dictionary from 2010 to 2018
        grades              (dict): The dictionary of grades from 2010 to 2018
        grade_count         (int): The grade count from 2010 to 2018
        average_grade       (float): The average grade from 2010 to 2018
        average_pass_rate   (float): The average pass rate from 2010 to 2018
        difficulty          (float): The difficulty of the course unit based in the data fetched. The difficulty is a float
                            value between 0.0 and 5.0. Lower the value lower the difficulty

    """

    def __init__(self, faculty, id, name, year, semester, code, acronym, credits):
        self.faculty = faculty
        self.id = id
        self.name = name
        self.year = year
        self.semester = semester
        self.code = code
        self.acronym = acronym
        self.credits = credits

        self.fetch_years(2010, 2019)
        self.calculate_grades()
        self.calculate_average_rate()
        self.calculate_difficulty()

    def fetch_years(self, starting_year, finishing_year):
        """
        Fetches the data from a single course unit instance from 2010 to 2018.

        This method retrives the data from each instance of the course unit taught from 2010 to 2018
        and then stores it in the years dictionary.
        """
        self.years = {}

        for year in range(2010, 2019):
            if self.faculty.verbosity is True:
                self.faculty.logger.info('Getting data for course unit instance with params: {}'.format(
                    {'name': self.name, 'year': year}
                ))

            course_unit_year = CourseUnitYear(self.faculty, self.id, year)

            self.years[year] = course_unit_year

    def calculate_grades(self):
        """
        Calculates the grades from 2010 to 2018.

        This method joins together the grade data from 2010 to 2018.
        """
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
        """
        Calculates the average grade.

        This method calculates the average grade from 2010 to 2018.
        """
        average = 0.0

        for key in self.grades:
            prob = self.grades[key] / self.grade_count

            average += prob * key

        self.average_grade = average

    def calculate_average_rate(self):
        """
        Calculates the average pass rate.

        This method calculates the average pass rate from 2010 to 2018.
        """
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

            if self.faculty.verbosity is True:
                self.faculty.logger.warning(
                    'Error while finding average pass rate')

            return

        self.average_pass_rate = sum / count

    def calculate_difficulty(self):
        """
        Calculates the difficulty rating of the course unit.

        Based on the average approve rate and grades from 2010 to 2018 the method computes a rating from 0.0 to 5.0 that
        represents the difficulty of each course unit. The lower the value lower the difficulty. The difficulty of the course unit
        is the weighted sum of 60% of the normalized average grade and 40% of the normalized pass rate.
        """
        if self.average_grade is None or self.average_pass_rate is None:
            self.difficulty = None

            if self.faculty.verbosity is True:
                self.faculty.logger.warning('Error while finding difficulty')

            return

        average_weighted = self.average_grade / 20.0 * 0.60
        pass_rate_weighted = self.average_pass_rate / 100.0 * 0.40

        self.difficulty = (average_weighted + pass_rate_weighted) * 5

    def json_object(self):
        """
        Creates a JSON object with the object data.

        This method transforms the object into a JSON object with every data stored in the class.
        """
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

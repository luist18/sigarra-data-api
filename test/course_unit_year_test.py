import unittest
import os
from dotenv import load_dotenv

from scrapper import Session, CourseUnitYear


class TestCourseUnitYear(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        self.session = Session(os.environ.get(
            'SCRAPPER_USER'), os.environ.get('SCRAPPER_PASSWORD'))

    def test_fetch_pass_rate(self):
        course_unit_year = CourseUnitYear(self.session, 436426, 2019)

        self.assertEqual(course_unit_year.pass_rate, 81.04)


if __name__ == '__main__':
    unittest.main()

import unittest
import os
from dotenv import load_dotenv

from scrapper import Session, Course, CourseUnit


class TestCourse(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        self.session = Session(os.environ.get(
            'SCRAPPER_USER'), os.environ.get('SCRAPPER_PASSWORD'))

    def test_informatica(self):
        course = Course(self.session, 2708)

        course.to_json('mieq.json')

        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()

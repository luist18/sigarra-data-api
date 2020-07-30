import unittest
import os

from scrapper import Session, Course, CourseUnit


class TestCourse(unittest.TestCase):

    def setUp(self):
        self.session = Session(os.environ.get('SCRAPPER_USER'), os.environ.get('SCRAPPER_PASSWORD'))

    def test_fetch_name(self):
        course = Course(self.session, 2496)
        
        self.assertEqual(course.name, 'Mestrado Integrado em Engenharia Informática e Computação')

if __name__ == '__main__':
    unittest.main()

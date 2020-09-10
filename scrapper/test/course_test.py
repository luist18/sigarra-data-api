#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import os
from dotenv import load_dotenv

from sigarra_data_scrapper import Faculty


class TestCourse(unittest.TestCase):

    def setUp(self):
        load_dotenv()

        auth = {
            'user': os.environ.get('SCRAPPER_USER'),
            'password': os.environ.get('SCRAPPER_PASSWORD')
        }

        self.faculty = Faculty(auth, 'FEUP', verbosity=True)

    def test_informatica(self):
        self.faculty.course_ids.append(2496)

        self.faculty.fetch_courses()

        course = self.faculty.courses[0]

        course.to_json('{}.json'.format(course.name))

        self.assertEqual(
            course.name, 'Mestrado Integrado em Engenharia Informática e Computação')


if __name__ == '__main__':
    unittest.main()

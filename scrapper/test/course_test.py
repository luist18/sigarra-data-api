#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import os
from dotenv import load_dotenv

from scrapper import Faculty


class TestCourse(unittest.TestCase):

    def setUp(self):
        load_dotenv()

        auth = {
            'user': os.environ.get('SCRAPPER_USER'),
            'password': os.environ.get('SCRAPPER_PASSWORD')
        }

        self.faculty = Faculty(
            auth, 'Faculdade de Engenharia da Universidade do Porto', 'FEUP')

    def test_quimica(self):
        self.faculty.course_ids.append(2708)

        self.faculty.fetch_courses()

        course = self.faculty.courses[0]

        self.assertEqual(
            course.name, 'Mestrado Integrado em Engenharia Química')


if __name__ == '__main__':
    unittest.main()

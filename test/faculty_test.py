import unittest
import os
from dotenv import load_dotenv

from scrapper import Session, Course, CourseUnit


class TestCourse(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        os.mkdir('data', 777)
        self.session = Session(os.environ.get(
            'SCRAPPER_USER'), os.environ.get('SCRAPPER_PASSWORD'))

    def test_bio(self):
        course = Course(self.session, 2475)

        course.to_json('data/mib.json')
        self.assertEqual(
            course.name, 'Mestrado Integrado em Bioengenharia')

    def test_civil(self):
        course = Course(self.session, 2480)

        course.to_json('data/miec.json')
        self.assertEqual(
            course.name, 'Mestrado Integrado em Engenharia Civil')

    def test_ambiente(self):
        course = Course(self.session, 2922)

        course.to_json('data/miea.json')
        self.assertEqual(
            course.name, 'Mestrado Integrado em Engenharia do Ambiente')

    def test_gestao(self):
        course = Course(self.session, 2678)

        course.to_json('data/miegi.json')
        self.assertEqual(
            course.name, 'Mestrado Integrado em Engenharia e Gestão Industrial')
    
    def test_eletro(self):
        course = Course(self.session, 2639)

        course.to_json('data/mieec.json')
        self.assertEqual(
            course.name, 'Mestrado Integrado em Engenharia Electrotécnica e de Computadores')

    def test_informatica(self):
        course = Course(self.session, 2496)

        course.to_json('data/mieic.json')
        self.assertEqual(
            course.name, 'Mestrado Integrado em Engenharia Informática e Computação')

    def test_mecanica(self):
        course = Course(self.session, 2484)

        course.to_json('data/miem.json')
        self.assertEqual(
            course.name, 'Mestrado Integrado em Engenharia Mecânica')

    def test_metal(self):
        course = Course(self.session, 2479)

        course.to_json('data/miemm.json')
        self.assertEqual(
            course.name, 'Mestrado Integrado em Engenharia Metalúrgica e de Materiais')

    def test_quimica(self):
        course = Course(self.session, 2708)

        course.to_json('data/mieq.json')
        self.assertEqual(
            course.name, 'Mestrado Integrado em Engenharia Química')


if __name__ == '__main__':
    unittest.main()

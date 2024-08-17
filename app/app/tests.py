""" Sample tests """


from django.test import SimpleTestCase
from app import calc


class TestCalc(SimpleTestCase):
    """ Test the calc app """
    def test_add_numbers(self):
        res = calc.add(5, 6)
        self.assertEqual(res, 11)

    def test_substract_numners(self):
        res = calc.substract(10, 15)
        self.assertEqual(res, -5)

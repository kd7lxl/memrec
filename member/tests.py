"""
This file tests the member application.
"""

from django.test import TestCase
from models import Person

class SimpleTest(TestCase):
    fixtures = ['test_data.json', ]
    
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)
    
    def test_retrive(self):
        """
        Tries to retrieve a known person object from the test fixture.
        """
        person = Person.objects.get(pk=144)
        self.failUnlessEqual(str(person), 'Kathleen Adams')

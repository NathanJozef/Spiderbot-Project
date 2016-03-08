import time
import datetime
import pickle
import os.path
from ClassLibrary.profiler import Profiler

class TestBuilder:

    switcher = {
        0: "Horizontal Line Test",
        1: "Vertical Line Test",
        2: "Diagonal Line Validation",
        3: "Accuracy Test"
        }

    def __init__(self):

        print '\n**** ENTER YOU INFORMATION ****\n'

        self.name = 'Nathan'
        self.conditions = 'Testing'
        self.profession = 'Engineer'

        #self.name = raw_input('Enter your name: ')
        #self.conditions = raw_input('Enter the conditions: ')
        #self.profession = raw_input('Enter your profession: ')
        print '\n**** SELECT THE TEST TYPE ****\n'
        print self.switcher
        self.testtype = int(raw_input('Enter test number: '))

        characteristic_profile = Profiler(self.name)

        self.linear_coefficients = characteristic_profile.linear_coefficients
        self.vertical_coefficients = characteristic_profile.vertical_coefficients
        self.accuracy_coefficients = characteristic_profile.accuracy_coefficients

    def __str__(self):

        return '\n' + 'Testee Name: ' + self.name + '\n' \
               + 'Conditions: ' + self.conditions + '\n' \
               + 'Profession: ' + self.profession + '\n' \
               + 'Test Type: ' + self.tests(self.testtype) + '\n' \
               + 'Horizontal Test Coefficients: ' + str(self.linear_coefficients) + '\n' \
               + 'Vertical Test Coefficients: ' + str(self.vertical_coefficients) + '\n' \
               + 'Accuracy Coefficients: ' + str(self.accuracy_coefficients) + '\n'

    def tests(self, a):
        return TestBuilder.switcher.get(a)

    def create_test_filename(self):

        filename = self.name + '_' \
                   + self.conditions + '_' \
                   + self.profession + '_' \
                   + self.tests(self.testtype) + '_' \
                   + time.strftime('%c')
        return filename
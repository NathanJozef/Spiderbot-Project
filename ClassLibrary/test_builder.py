class TestBuilder:

    switcher = {
        0: "Simple Line Test",
        1: "Diagonal Line Test"
        }

    def __init__(self):

        print '**** SELECT THE TEST TYPE ****\n'
        print self.switcher

        self.name = 'Nathan'
        self.conditions = 'Testing'
        self.profession = 'Engineer'

        self.testtype = int(raw_input('Enter test number: '))
        #self.name = raw_input('Enter your name: ')
        #self.conditions = raw_input('Enter the conditions: ')
        #self.profession = raw_input('Enter your profession: ')

    def __str__(self):

        return '\n' + 'Testee Name: ' + self.name + '\n' \
               + 'Conditions: ' + self.conditions + '\n' \
               + 'Profession: ' + self.profession + '\n' \
               + 'Test Type: ' + self.tests(self.testtype) + '\n'

    def tests(self, a):
        return TestBuilder.switcher.get(a)
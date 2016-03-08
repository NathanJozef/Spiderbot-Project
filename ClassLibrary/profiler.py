import pickle
import os.path

class Profiler():

    def __init__(self, name):

        self.testee = name
        self.profile_filename = 'Profile_' + self.testee
        self.linear_coefficients = [1, 1, 1]
        self.vertical_coefficients = [1, 1, 1]
        self.diagonal_coefficients = [1, 1, 1]
        self.accuracy_coefficients = [1, 1, 1]

        if os.path.exists('Profiles/' + self.profile_filename):
            self.open_existing_file()

    def open_existing_file(self):

        picklefile = open('Profiles/' + self.profile_filename, 'rb')
        tmp_dict = pickle.load(picklefile)
        picklefile.close()
        self.__dict__.update(tmp_dict)

    def write_linear_coefficients(self, coefficients):

        print '\nUpdating linear Coefficients\n'

        if self.linear_coefficients == [1, 1, 1]:
            self.linear_coefficients[0] = float('{0:.2f}'.format(coefficients[0]))
            self.linear_coefficients[1] = float('{0:.2f}'.format(coefficients[1]))
            self.linear_coefficients[2] = float('{0:.2f}'.format(coefficients[2]))
        elif self.linear_coefficients != [1, 1, 1]:
            self.linear_coefficients[0] = float('{0:.2f}'.format((coefficients[0] + self.linear_coefficients[0]) / 2))
            self.linear_coefficients[1] = float('{0:.2f}'.format((coefficients[1] + self.linear_coefficients[1]) / 2))
            self.linear_coefficients[2] = float('{0:.2f}'.format((coefficients[2] + self.linear_coefficients[2]) / 2))

        self.save_to_picklefile()

    def write_vertical_coefficients(self, coefficients):

        print '\nUpdating vertical Coefficients\n'

        if self.vertical_coefficients == [1, 1, 1]:
            self.vertical_coefficients[0] = float('{0:.2f}'.format(coefficients[0]))
            self.vertical_coefficients[1] = float('{0:.2f}'.format(coefficients[1]))
            self.vertical_coefficients[2] = float('{0:.2f}'.format(coefficients[2]))
        elif self.vertical_coefficients != [1, 1, 1]:
            self.vertical_coefficients[0] = float('{0:.2f}'.format((coefficients[0] + self.vertical_coefficients[0]) / 2))
            self.vertical_coefficients[1] = float('{0:.2f}'.format((coefficients[1] + self.vertical_coefficients[1]) / 2))
            self.vertical_coefficients[2] = float('{0:.2f}'.format((coefficients[2] + self.vertical_coefficients[2]) / 2))

        self.save_to_picklefile()

    def save_to_picklefile(self):

        picklefile = open('Profiles/' + self.profile_filename, 'wb')
        pickle.dump(self.__dict__, picklefile)
        picklefile.close()





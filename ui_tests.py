import generator_motor_test as gen
import time
from ClassLibrary.test_builder import TestBuilder

test_instance = TestBuilder()
print test_instance

print 'Test Beginnning in 5 Seconds...'
time.sleep(1)
print '4'
time.sleep(1)
print '3'
time.sleep(1)
print '2'
time.sleep(1)
print '1'
time.sleep(1)

gen.generator(test_instance)


import unittest

if __name__ == '__main__':

	load = unittest.TestLoader()
	test = load.discover('test/')
	run = unittest.runner.TextTestRunner()
	run.run(test)
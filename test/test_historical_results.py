from historical_results import HistoricalResults
import unittest2
import pdb
import os


class TestReadInResults(unittest2.TestCase):

    def test_file_does_not_exist(self):
        h = HistoricalResults()
        results = h.read_in_prev_results("foo")
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 0)

    def test_read_in_results_1(self):
    	# Dummy file 
    	filename = "foo"

    	# Give it some data
    	lines = [
    		"foo\t2018-09-28 19:54:10 CDT\t10/10\t75.0*",
    		"bar\t2018-09-28 16:32:32 CDT\t9/10\t90.0*",
    		"foo\t2018-10-03 17:52:45 CDT\t8/10\t85.0*"
    	]

    	# Save the dummy data
    	with open(filename, 'w') as f:
    		for line in lines:
    			f.write(line + "\n")

    	# Read from the same file
    	h = HistoricalResults()
    	results = h.read_in_prev_results(filename)

    	# Make assertions
    	self.assertDictEqual(
    		results,
    		{
	    		'foo': {
	    			'10/10': [
	    				['2018-09-28 19:54:10 CDT', '75.0*']
	    			], 
	    			'8/10': [
	    				['2018-10-03 17:52:45 CDT', '85.0*']
	    			]
	    		}, 
	    		'bar': {
	    			'9/10': [
	    				['2018-09-28 16:32:32 CDT', '90.0*']
	    			]
    			}
    		}
    	)
    	

    	# Remove the dummy file
    	os.remove(filename)

    def test_read_in_results_1(self):
    	# Dummy file 
    	filename = "foo"

    	# Give it some data
    	lines = [
    		"foo\t2018-09-28 19:54:10 CDT\t10/10\t75.0",
    		"foo\t2018-09-28 16:32:32 CDT\t10/10\t74.0*",
    		"foo\t2018-10-03 17:52:45 CDT\t10/10\t85.0"
    	]

    	# Save the dummy data
    	with open(filename, 'w') as f:
    		for line in lines:
    			f.write(line + "\n")

    	# Read from the same file
    	h = HistoricalResults()
    	results = h.read_in_prev_results(filename)

    	# Make assertions
    	self.assertDictEqual(
    		results,
    		{
	    		'foo': {
	    			'10/10': [
	    				['2018-09-28 19:54:10 CDT', '75.0'],
	    				['2018-09-28 16:32:32 CDT', '74.0*'],
	    				['2018-10-03 17:52:45 CDT', '85.0']
	    			]
    			}
    		}
    	)
    	

    	# Remove the dummy file
    	os.remove(filename)

if __name__ == '__main__':
    unittest2.main()
import re
import sys

"""
Purposes of this program:
- Calculate billable hours with minute accuracy.
- Teach myself Python (again)
"""

# Transform HH:MMxm notation into minutes
time_regex = re.compile("(\d+):(\d+)(\S+)")
def minutes(time):
	match = time_regex.match(time)
	h = match.groups()[0]
	m = match.groups()[1]
	ampm = match.groups()[2]

	hours = int(h)
	if hours == 12:
		hours = 0

	minutes = int(m)
	if ampm == "pm":
		minutes += 12*60
	minutes += hours*60

	return minutes

# Transform time - time range notation into minutes
range_regex = re.compile("(.*) - (.*)")
def range(timerange):
	match = range_regex.match(timerange)
	begin = match.groups()[0]
	end = match.groups()[1]

	begin = minutes(begin)
	end = minutes(end)
	
	return end - begin

# Transform list of HH:MMxm ranges into minute total
ranges_regex = re.compile("(\d+:\d+.m - \d+:\d+.m)")
def multirange(timeranges):
	print timeranges
	matches = ranges_regex.findall(timeranges)
	if len(matches) > 0:
		total_minutes = reduce(lambda x,y:x+y, map(range, matches))
		print " " + str(total_minutes) + "\n"
		return total_minutes
	else:
		return 0

# Transform file of time ranges into total hours
def read_timesheet(timesheet):
	file = open(timesheet,"r")
	print reduce(lambda x,y:x+y, map(multirange,file))/60.0

def main(filename):
	print filename
	read_timesheet(filename)

if __name__ == '__main__':
	if len(sys.argv) == 2 :
		main(sys.argv[1])

"""
Tests
"""
def test(statement):
	if statement:
		result = "Pass"
	else:
		result = "Fail"
	return result

def print_failed(method, status):
	if status == "Fail":
		print method + "failed"

def run_tests():
	# 13.5 * 60 = 810
	print_failed("minutes", str(test(810 == minutes("1:30pm"))))

	# 12*60 = 720
	print_failed("range", str(test(720 == range("1:30am - 1:30pm"))))

	# 61 + 60*12-1 = 780
	print_failed("multirange", str(test(780 == multirange("5:00am - 6:01am, 7:00am - 6:59pm"))))

	# 12:00am - 1:10am, 10:37am - 12:54pm, 1:33pm - 7:00pm
	# (13*60+10) - 12*60 + (12*60 + 54) - (10*60 + 37) + 19*60 - (13*60+33) = 534
	print_failed("multirange2", str(test(534 == multirange("12:00am - 1:10am, 10:37am - 12:54pm, 1:33pm - 7:00pm"))))

	# 12:01am = minute 1
	print_failed("ampm test", str(test(1 == minutes("12:01am"))))

	# 12:00am = minute 0
	print_failed("ampm test 2", str(test(0 == minutes("12:00am"))))


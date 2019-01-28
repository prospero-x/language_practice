import os
from stat import S_ISDIR
from enum import Enum
import sys


class DirectoryStatus(Enum):
	STATUS_OK = 0
	NOT_FOUND = 1
	NOT_A_DIRECTORY = 2
	UNKOWN_ERROR = 3


def validate_directory(dirname):
	try:
		mode = os.stat(dirname).st_mode
		if not S_ISDIR(mode):
			return DirectoryStatus.NOT_A_DIRECTORY
	except FileNotFoundError:
		return DirectoryStatus.NOT_FOUND

	except Exception as e:
		print(type(e), e)
		return DirectoryStatus.UNKNOWN_ERROR


if __name__ == '__main__':
	result = validate_directory(sys.argv[1])
	print(result)

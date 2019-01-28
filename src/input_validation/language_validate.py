from enum import Enum
from directory import DirectoryStatus, verify_directory


class LanguageStatus(Enum):
	STATUS_OK = 0


def validate_language(language_name):
	#  Verify language value is a directory in 'languages'
	result = verify_directory('languages/%s' % language_name)

	if result == DirectoryStatus.NOT_FOUND:
		pass
	elif result == DirectoryStatus.NOT_A_DIRECTORY:
		pass
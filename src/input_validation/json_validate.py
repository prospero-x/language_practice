import json
import sys
from enum import Enum


class JSONStatus(Enum):
	STATUS_OK = 0
	NOT_FOUND = 1
	NOT_A_VALID_JSON = 2
	UNKNOWN_ERROR = 3


def validate_json(fname):
	try:
		with open(fname, 'r') as f:
			json.load(f)
		return JSONStatus.STATUS_OK

	except json.decoder.JSONDecodeError:
		return JSONStatus.NOT_A_VALID_JSON

	except FileNotFoundError:
		return JSONStatus.NOT_FOUND

	except Exception as e:
		print(type(e), e)
		return JSONStatus.UNKNOWN_ERROR


if __name__ == '__main__':
	result = validate_json(sys.argv[1])
	print(result)
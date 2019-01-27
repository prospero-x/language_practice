import json
import sys
from output_color import OutputColor

if __name__ == '__main__':
	with open(sys.argv[1]) as f:
		try: 
			json.load(f)
			print(OutputColor.GREEN + "Valid json!" + OutputColor.END_COLOR)
		except: 
			print(OutputColor.RED + "Invalid Json." + OutputColor.END_COLOR)
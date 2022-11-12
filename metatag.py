from enum import Enum
from glob import glob
from os import stat, path, rename
from time import strftime, localtime


class Mode(Enum):
	SIZE = 6
	ACCESS = 7
	MODIFICATION = 8
	CREATION = 9

def renameFiles(files, mode, seperator):
	for file in files:
		try:
			# d = open(file)
			pass
		except:
			print("File not found")

		old = path.realpath(file)
		root, ext = path.splitext(old)
		meta = stat(file)

		match mode:
			case Mode.SIZE:
				appendix = f"{meta[mode.value]}Byte"
			case Mode.ACCESS | Mode.MODIFICATION | Mode.CREATION:
				raw = meta[mode.value]
				time = localtime(raw)
				appendix = strftime("%Y-%m-%d", time)
			case _:
				print("No mode defined")
				return

		new = f"{root}{seperator}{appendix}{ext}"
		print(f"Old:\t{old}\nNew:\t{new}")
		# rename(old, new)
		# d.close()


pth = path.dirname(__file__) # = input("Directory: ")

# rename all txt files in directory to size
files = glob(f"{pth}/*.txt")
renameFiles(files, Mode.SIZE, "_")

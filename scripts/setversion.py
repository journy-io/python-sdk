import re
import sys


def rename_version(filename, new_version):
    with open(filename, "r") as file:
        lines = file.readlines()
    lines = list(map(lambda str: re.sub(r'version="[0-9\.]*"', 'version="' + new_version + '"', str), lines))
    with open(filename, "w") as file:
        file.writelines(lines)


if __name__ == "__main__":
    filename, new_version = sys.argv[1], sys.argv[2]
    rename_version(filename, new_version)
    print("Done editing version")

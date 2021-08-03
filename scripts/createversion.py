import sys


def create_version(version):
    with open("journyio/version.py", "w") as file:
        file.write(f"version = \"{version}\"\n")


if __name__ == "__main__":
    version = sys.argv[1]
    create_version(version)
    print("Done creating version file")

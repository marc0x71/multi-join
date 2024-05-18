#! /bin/env python


import argparse
from project.file_handler import FileHandler
from project.join import join_files


def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--files", required=True, nargs="+", default=[])
    ap.add_argument("-k", "--keys", required=True, nargs="+", default=[])
    ap.add_argument("-s", "--separator", default=",")
    args = vars(ap.parse_args())

    files = args["files"]
    keys = args["keys"]
    separator = args["separator"]

    if len(files) != len(keys):
        print("Invalid files/keys, must have same length")
        exit(1)

    if len(files) < 2:
        print("Invalid files/keys, you should provide more than one file")
        exit(1)

    if not all(x.isnumeric() for x in keys):
        print("Invalid keys, must be numbers")
        exit(1)
    
    if len(separator) > 1:
        print("Invalid separator length")
        exit(1)

    file_handlers = [
        FileHandler(filename=filename, key_position=int(key), separator=separator)
        for filename, key in zip(files, keys)
    ]

    for lines in join_files(file_handlers):
        print(lines)


if __name__ == "__main__":
    main()

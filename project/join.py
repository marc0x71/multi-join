from typing import Generator, List, Optional

from file_handler import FileHandler


def join_files(files: List[FileHandler]):# -> Generator[List[Optional[str]], None, None]:
    for file in files:
        file.open()

    master = files[0]
    others = files[1:]

    for value, line in master.readlines():
        while True:
            got = [other.validate(value) for other in others]
            
            if all(x == None for x in got):
                break
            
            yield [line] + got

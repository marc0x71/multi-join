from typing import Optional


class FileHandler:
    filename: str
    key_position: int
    separator: str
    eof: bool = False
    __fd = None  # type: ignore[override]
    __value: Optional[str] = None
    __line: Optional[str] = None

    def __init__(self, filename: str, key_position: int, separator: str = "|") -> None:
        self.filename = filename
        self.key_position = key_position
        self.separator = separator

    def __del__(self):
        if self.__fd is not None:
            self.__fd.close()

    def open(self):
        self.__fd = open(self.filename, "r", encoding="utf-8")

    def readline(self) -> Optional[str]:
        line = self.__fd.readline()  # type: ignore[override]
        if not line:
            self.eof = True
            return None
        return line.strip()

    def __read(self) -> None:
        self.__value = None
        self.__line = None

        row = self.readline()
        if not row:
            return

        self.__line = row.strip()
        v = self.__line.split(self.separator)
        if len(v) > self.key_position:
            self.__value = v[self.key_position]

    def readlines(self):
        while True:
            self.__read()
            if not self.__line:
                break

            yield self.__value, self.__line

    def validate(self, value: str) -> Optional[str]:
        if self.eof:
            return None

        if self.__value is None or self.__value < value:
            self.__read()

        while self.__value is not None and self.__value < value:
            self.__read()

        if self.__value == value:
            result = self.__line
            self.__value = None
            self.__line = None
            return result
        return None

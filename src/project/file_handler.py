from typing import Optional


class FileHandler:
    __filename: str
    __key_position: int
    __separator: str
    __fd = None  # type: ignore[override]
    __eof: bool = False
    __value: Optional[str] = None
    __line: Optional[str] = None

    def __init__(self, filename: str, key_position: int, separator: str = "|") -> None:
        self.__filename = filename
        self.__key_position = key_position
        self.__separator = separator

    def __del__(self):
        if self.__fd is not None:
            self.__fd.close()

    def open(self):
        self.__fd = open(self.__filename, "r", encoding="utf-8")

    def readline(self) -> Optional[str]:
        line = self.__fd.readline()  # type: ignore[override]
        if not line:
            self.__eof = True
            return None
        return line.strip()

    def __read(self) -> None:
        self.__value = None
        self.__line = None

        row = self.readline()
        if not row:
            return

        self.__line = row.strip()
        v = self.__line.split(self.__separator)
        if len(v) > self.__key_position:
            self.__value = v[self.__key_position]

    def readlines(self):
        while True:
            self.__read()
            if not self.__line:
                break

            yield self.__value, self.__line

    def validate(self, value: str) -> Optional[str]:
        if self.__eof:
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

    @property
    def eof(self):
        return self.__eof

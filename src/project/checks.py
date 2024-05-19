from typing import Callable, Optional, Protocol


ChecksFailedCallbackFn = Callable[[str, str], None]


class Checker(Protocol):
    def check(self, new_value: str) -> None:
        pass


class IsSortedChecker:
    __previous: Optional[str] = None
    __sorted: bool = True
    __callback: ChecksFailedCallbackFn
    __filename: str

    def __init__(self, filename: str, callback: ChecksFailedCallbackFn) -> None:
        self.__filename = filename
        self.__callback = callback

    def check(self, new_value: str) -> None:
        if not self.__previous:
            self.__previous = new_value
            return
        if self.__sorted:
            self.__sorted = self.__previous <= new_value
            if not self.__sorted:
                self.__callback(self.__filename, "not sorted")
        self.__previous = new_value


CheckerBuilderFn = Callable[[str, ChecksFailedCallbackFn], Checker]


def build_sorted_checker(filename: str, callback: ChecksFailedCallbackFn) -> Checker:
    return IsSortedChecker(filename=filename, callback=callback)


def checks_fails(filename: str, error: str) -> None:
    print(f"WARNING! Checks fails on [{filename}]: {error}")

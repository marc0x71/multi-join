from io import StringIO
from unittest.mock import MagicMock, patch

from project.checks import IsSortedChecker, build_sorted_checker, checks_fails


@patch("project.file_handler.ChecksFailedCallbackFn")
@patch("project.checks.IsSortedChecker")
def test_build_sorted_checker(
    mocked_is_sort_checker: MagicMock, mocked_callback: MagicMock
):
    got = build_sorted_checker("filename", mocked_callback)
    mocked_is_sort_checker.assert_called_once_with(
        filename="filename", callback=mocked_callback
    )
    assert got == mocked_is_sort_checker()


@patch("project.file_handler.ChecksFailedCallbackFn")
def test_is_sorted_no_call(mocked_callback: MagicMock):
    checker = IsSortedChecker("filename", mocked_callback)

    for value in ["1", "2", "3"]:
        checker.check(value)

    mocked_callback.assert_not_called()


@patch("project.file_handler.ChecksFailedCallbackFn")
def test_is_sorted_single_value_unexpected(mocked_callback: MagicMock):
    checker = IsSortedChecker("filename", mocked_callback)

    for value in ["1", "2", "5", "3"]:
        checker.check(value)

    mocked_callback.assert_called_once_with("filename", "not sorted")


@patch("project.file_handler.ChecksFailedCallbackFn")
def test_is_sorted_more_values_unexpected(mocked_callback: MagicMock):
    checker = IsSortedChecker("filename", mocked_callback)

    for value in ["1", "2", "5", "3", "4", "2"]:
        checker.check(value)

    mocked_callback.assert_called_once_with("filename", "not sorted")


def test_checks_fails():
    with patch("sys.stdout", new_callable=StringIO) as mocked_stdout:
        checks_fails("filename", "message")

    assert mocked_stdout.getvalue() == "WARNING! Checks fails on [filename]: message\n"

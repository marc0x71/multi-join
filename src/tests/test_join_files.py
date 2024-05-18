from unittest.mock import MagicMock, patch

from project.join import join_files


def test_join_files_basic():
    files = [MagicMock(id=x) for x in range(3)]

    master = files[0]
    master.readlines = MagicMock(
        return_value=[
            ("0", "0|master0"),
            ("1", "1|master1"),
            ("2", "2|master2"),
        ]
    )

    files[1].validate.side_effect = iter(
        ["0|first0", None, None, None, "2|first2", None]
    )
    files[2].validate.side_effect = iter(
        ["0|second0", None, "1|second1", None, None, None]
    )
    files[1].eof = False
    files[2].eof = False

    got = []
    for values in join_files(files):
        got.append(values)

    exp = [
        ["0|master0", "0|first0", "0|second0"],
        ["1|master1", None, "1|second1"],
        ["2|master2", "2|first2", None],
    ]

    assert got == exp


def test_join_files_no_match():
    files = [MagicMock(id=x) for x in range(3)]

    master = files[0]
    master.readlines = MagicMock(
        return_value=[
            ("0", "0|master0"),
            ("1", "1|master1"),
            ("2", "2|master2"),
        ]
    )

    files[1].validate.side_effect = iter([None, None, None, None, None, None])
    files[2].validate.side_effect = iter([None, None, None, None, None, None])
    files[1].eof = False
    files[2].eof = False

    got = []
    for values in join_files(files):
        got.append(values)

    exp = [
        ["0|master0", None, None],
        ["1|master1", None, None],
        ["2|master2", None, None],
    ]

    assert got == exp


def test_join_files_multiple():
    files = [MagicMock(id=x) for x in range(3)]

    master = files[0]
    master.readlines = MagicMock(
        return_value=[
            ("0", "0|master0"),
            ("1", "1|master1"),
            ("2", "2|master2"),
        ]
    )

    files[1].validate.side_effect = iter(
        ["0|first01", "0|first02", None, None, None, "2|first2", None]
    )
    files[2].validate.side_effect = iter(
        ["0|second0", None, None, "1|second1", None, None, None]
    )
    files[1].eof = False
    files[2].eof = False

    got = []
    for values in join_files(files):
        got.append(values)

    exp = [
        ["0|master0", "0|first01", "0|second0"],
        ["0|master0", "0|first02", None],
        ["1|master1", None, "1|second1"],
        ["2|master2", "2|first2", None],
    ]

    assert got == exp

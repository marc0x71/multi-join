from unittest.mock import MagicMock, patch

from project.file_handler import FileHandler


def test_file_handler_open_close():
    file = MagicMock()
    with patch("builtins.open", return_value=file, create=True) as mock_file:
        handler = FileHandler(filename="test_file", key_position=0, separator="|")
        handler.open()
        mock_file.assert_called_once_with("test_file", "r", encoding="utf-8")
        del handler
        file.close.assert_called_once()


def test_file_handler_readlines():
    file = MagicMock()
    file.readline.side_effect = iter(["1|first", "2|second", "3|third", ""])
    with patch("builtins.open", return_value=file, create=True) as mock_file:
        handler = FileHandler(filename="test_file", key_position=0, separator="|")
        handler.open()
        mock_file.assert_called_once_with("test_file", "r", encoding="utf-8")

        got = []
        for x in handler.readlines():
            got.append(x)

        del handler
        file.close.assert_called_once()

        exp = [
            ("1", "1|first"),
            ("2", "2|second"),
            ("3", "3|third"),
        ]
        assert got == exp


def test_file_handler_validate_normal():
    file = MagicMock()
    file.readline.side_effect = iter(["1|first", "2|second", "3|third", ""])
    with patch("builtins.open", return_value=file, create=True) as mock_file:
        handler = FileHandler(filename="test_file", key_position=0, separator="|")
        handler.open()
        mock_file.assert_called_once_with("test_file", "r", encoding="utf-8")

        values = ["1", "2", "3"]
        got = []
        for value in values:
            got.append(handler.validate(value))

        assert not handler.eof

        del handler
        file.close.assert_called_once()

        exp = ["1|first", "2|second", "3|third"]
        assert exp == got


def test_file_handler_validate_last_missing():
    file = MagicMock()
    file.readline.side_effect = iter(["1|first", "2|second", "3|third", ""])
    with patch("builtins.open", return_value=file, create=True) as mock_file:
        handler = FileHandler(filename="test_file", key_position=0, separator="|")
        handler.open()
        mock_file.assert_called_once_with("test_file", "r", encoding="utf-8")

        values = ["1", "2", "3", "5"]
        got = []
        for value in values:
            got.append(handler.validate(value))

        assert handler.eof

        del handler
        file.close.assert_called_once()

        exp = ["1|first", "2|second", "3|third", None]
        assert exp == got


def test_file_handler_validate_eof():
    file = MagicMock()
    file.readline.side_effect = iter(["1|first", "2|second", "3|third", ""])
    with patch("builtins.open", return_value=file, create=True) as mock_file:
        handler = FileHandler(filename="test_file", key_position=0, separator="|")
        handler.open()
        mock_file.assert_called_once_with("test_file", "r", encoding="utf-8")

        values = ["1", "2", "3", "4", "5"]
        got = []
        for value in values:
            got.append(handler.validate(value))

        assert handler.eof

        del handler
        file.close.assert_called_once()

        exp = ["1|first", "2|second", "3|third", None, None]
        assert exp == got


def test_file_handler_validate_with_gap_middle():
    file = MagicMock()
    file.readline.side_effect = iter(["1|first", "5|second", "6|third", ""])
    with patch("builtins.open", return_value=file, create=True) as mock_file:
        handler = FileHandler(filename="test_file", key_position=0, separator="|")
        handler.open()
        mock_file.assert_called_once_with("test_file", "r", encoding="utf-8")

        values = ["1", "2", "3", "4", "5", "6"]
        got = []
        for value in values:
            got.append(handler.validate(value))

        assert not handler.eof

        del handler
        file.close.assert_called_once()

        exp = ["1|first", None, None, None, "5|second", "6|third"]
        assert exp == got


def test_file_handler_validate_with_gap_first():
    file = MagicMock()
    file.readline.side_effect = iter(["4|first", "5|second", "6|third", ""])
    with patch("builtins.open", return_value=file, create=True) as mock_file:
        handler = FileHandler(filename="test_file", key_position=0, separator="|")
        handler.open()
        mock_file.assert_called_once_with("test_file", "r", encoding="utf-8")

        values = ["1", "2", "3", "4", "5", "6"]
        got = []
        for value in values:
            got.append(handler.validate(value))

        assert not handler.eof

        del handler
        file.close.assert_called_once()

        exp = [None, None, None, "4|first", "5|second", "6|third"]
        assert exp == got


def test_file_handler_validate_with_gap_last():
    file = MagicMock()
    file.readline.side_effect = iter(["6|third", ""])
    with patch("builtins.open", return_value=file, create=True) as mock_file:
        handler = FileHandler(filename="test_file", key_position=0, separator="|")
        handler.open()
        mock_file.assert_called_once_with("test_file", "r", encoding="utf-8")

        values = ["1", "2", "3", "4", "5", "6"]
        got = []
        for value in values:
            got.append(handler.validate(value))

        assert not handler.eof

        del handler
        file.close.assert_called_once()

        exp = [None, None, None, None, None, "6|third"]
        assert exp == got

def test_file_handler_validate_with_gap_single():
    file = MagicMock()
    file.readline.side_effect = iter(["1|gap1", "4|first", "5|second", "6|third", ""])
    with patch("builtins.open", return_value=file, create=True) as mock_file:
        handler = FileHandler(filename="test_file", key_position=0, separator="|")
        handler.open()
        mock_file.assert_called_once_with("test_file", "r", encoding="utf-8")

        values = [".", "4", "5", "6"]
        got = []
        for value in values:
            got.append(handler.validate(value))

        assert not handler.eof

        del handler
        file.close.assert_called_once()

        exp = [None, "4|first", "5|second", "6|third"]
        assert exp == got

def test_file_handler_validate_with_gap_double():
    file = MagicMock()
    file.readline.side_effect = iter(["1|gap1", "2|gap2", "4|first", "5|second", "6|third", ""])
    with patch("builtins.open", return_value=file, create=True) as mock_file:
        handler = FileHandler(filename="test_file", key_position=0, separator="|")
        handler.open()
        mock_file.assert_called_once_with("test_file", "r", encoding="utf-8")

        values = [".", "4", "5", "6"]
        got = []
        for value in values:
            got.append(handler.validate(value))

        assert not handler.eof

        del handler
        file.close.assert_called_once()

        exp = [None, "4|first", "5|second", "6|third"]
        assert exp == got

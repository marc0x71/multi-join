from unittest.mock import MagicMock, patch

from project.file_handler import FileHandler


def test_file_handler_open_close():
    file = MagicMock()
    with patch("builtins.open", return_value=file, create=True) as mock_file:
        handler = FileHandler(filename="test_file", key_position=0, separator="|")
        handler.open()
        mock_file.assert_called_once_with("test_file", "r", encoding='utf-8')
        del(handler)
        file.close.assert_called_once()
        
def test_file_handler_readlines():
    file = MagicMock()
    file.readline.side_effect = iter(["1|first", "2|second", "3|third", ""])
    with patch("builtins.open", return_value=file, create=True) as mock_file:
        handler = FileHandler(filename="test_file", key_position=0, separator="|")
        handler.open()
        mock_file.assert_called_once_with("test_file", "r", encoding='utf-8')
        
        got = []
        for x in handler.readlines():
            got.append(x)
                    
        del(handler)
        file.close.assert_called_once()
        
        exp = [
            ('1', '1|first'),
            ('2', '2|second'),
            ('3', '3|third'),
        ]
        assert got == exp
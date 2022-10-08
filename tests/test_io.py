import pytest
from backblaze_backups.io import Io

def test_exception_file_not_found():
    io = Io()
    with pytest.raises(FileNotFoundError):
        io.open_file("random")

def test_no_exception_file_found(config_path):
    io = Io()
    config = io.open_file(config_path)
    assert config != ""
from app.config import config
import pytest

def test_empty_API_Error():
    with pytest.raises(Exception):
        config.chatgpt_api_key

def test_no_correct_path_provided():
    with pytest.raises(RuntimeError):
        config.data_dir = "wrongFolderName"

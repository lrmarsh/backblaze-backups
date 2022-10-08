import pytest
from backblaze_backups.config import Config, ConfigManager

def test_config_is_loaded(config_path):
    configmanager = ConfigManager(config_path)
    assert type(configmanager.config) == Config
    assert configmanager.config.application_key == '123'
    assert configmanager.config.application_key_id == '123'
    assert configmanager.config.buckets == ['abc:dfg']
    assert configmanager.buckets[0].local == 'abc'
    assert configmanager.buckets[0].remote == 'dfg'
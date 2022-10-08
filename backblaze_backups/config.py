from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List
from backblaze_backups.io import Io

@dataclass
class Bucket:
    local: str
    remote: str


@dataclass_json
@dataclass
class Config:
    application_key_id: str
    application_key: str
    buckets: List[str]


class ConfigManager:
    def __init__(self, config_path: str):
        self.io = Io()
        self.config = self._load_config(config_path)
        self.buckets = self._parse_buckets()

    def _load_config(self, path: str) -> Config:
        try:
            config = self.io.open_file(path)
            return Config.from_json(config)
        except Exception as ex:
            print(f"Problem loading config {ex}")
    
    def _parse_buckets(self) -> List[Bucket]:
        buckets: List[Bucket] = list()
        for bucket in self.config.buckets:
            local_remote = bucket.split(":")
            if len(local_remote) != 2:
                raise ConfigException(f"Buckets are not in the correct format: Expexted local:remote. Got: {local_remote}")
            
            buckets.append(Bucket(local_remote[0], local_remote[1]))

        return buckets

class ConfigException(Exception):
    pass
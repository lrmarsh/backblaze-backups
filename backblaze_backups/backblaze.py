from typing import List
from b2sdk.v2 import (B2Api, CompareVersionMode, InMemoryAccountInfo,
                      KeepOrDeleteMode, NewerFileSyncMode, ScanPoliciesManager,
                      Synchronizer, SyncReport, parse_sync_folder)

from backblaze_backups.config import ConfigManager
from backblaze_backups.io import Io
import sys
import time
from datetime import datetime

now = datetime.now()

B2_PREFIX = "b2://"


class BackblazeBackup:
    def __init__(self) -> None:
        self.io = Io()
        self.config = ConfigManager(f'{self.io.get_root()}/config.json')
        self.bb = B2Api(InMemoryAccountInfo())
        self._auth()
        self.buckets = self._list_buckets()
        self.synchronizer = Synchronizer(max_workers=10, policies_manager=ScanPoliciesManager(exclude_all_symlinks=True), dry_run=False, allow_empty_source=True,
                                         compare_version_mode=CompareVersionMode.SIZE, compare_threshold=10, newer_file_mode=NewerFileSyncMode.REPLACE, keep_days_or_delete=KeepOrDeleteMode.DELETE)

    def _auth(self):
        self.bb.authorize_account(
            "production", self.config.config.application_key_id, self.config.config.application_key)

    def _list_buckets(self) -> List[str]:
        buckets = self.bb.list_buckets()
        remote_buckets: List[str] = list()

        for bucket in buckets:
            remote_buckets.append(bucket.name)
        return remote_buckets

    def backup(self):
        source_destination = []
        for bucket in self.config.buckets:
            if not self.io.path_exists(bucket.local):
                raise FileNotFoundError(bucket.local)

            if not bucket.remote in self.buckets:
                self.bb.create_bucket(bucket.remote, "allPrivate")

            source_destination.append((parse_sync_folder(
                bucket.local, self.bb), parse_sync_folder(f"{B2_PREFIX}{bucket.remote}", self.bb)))

        sys.stdout.write(
            f"Starting backup at:{now.strftime('%m/%d/%Y, %H:%M:%S')}")
        with SyncReport(sys.stdout, False) as reporter:
            for source, destination in source_destination:
                self.synchronizer.sync_folders(
                    source_folder=source,
                    dest_folder=destination,
                    now_millis=int(round(time.time() * 1000)),
                    reporter=reporter,
                )
        sys.stdout.write(f"Finished backup at:{now.strftime('%m/%d/%Y, %H:%M:%S')}")                


def backup():
    bb = BackblazeBackup()
    bb.backup()

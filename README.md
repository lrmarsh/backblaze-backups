# Backblaze backups

Provides a small wrapper around backblaze python SDK.
Provides a small util to move photo, videos and documents to different dirs.

- Local directories are check they exist, but are not created.
- Remote buckets are created if they do not exist, defauled to private.

# Getting started

## Requirements

 - Backblaze creds
 - poetry
 - python ^3.8

## Installation

Run `poetry install`


## Running backups

1. Add your `application_key_id` and `application_key` to the `config.json`
2. Add buckets to be mapping, its similar to docker mounting. Example /local/dir:bb_bucket
3. run `poertry backup`

## Running sort

`poetry run sort`

### Arguments
- `--root_dir` Directory to start the search in, default .
- `--photos_dir` Directory to move photos, default is ./photos
- `--videos_dir` Directory to move videos, default is ./videos
- `--docs_dir` Directory to move docs, default is ./docs

Run `poetry run sort -h` to see full list of arugments

Example: `poetry run sort --root_dir /home/ --photos_dir /home/photos --videos_dir /home/videos --docs_dir /home/docs`

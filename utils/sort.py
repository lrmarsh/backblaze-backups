from datetime import datetime
from os import walk
from os.path import exists
import shutil
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--root_dir', default=".", type=str,
                    help='Root directory to search, default is .')
parser.add_argument('--photos_dir', default="./photos", type=str,
                    help='Directory to move photos, default is ./photos')
parser.add_argument('--videos_dir', default="./videos", type=str,
                    help='Directory to move videos, default is ./videos')
parser.add_argument('--docs_dir', default="./docs", type=str,
                    help='Directory to move docs, default is ./docs')

photo_extensions = ["jpg", "jpeg", "png", "gif",
                    "tiff", "psd", "eps", "ai", "raw"]

video_extensions = ["mp4", "mov", "wmv", "avi", "avchd", "mkv", "webm"]

doc_extensions = ["pdf", "doc", "docx"]

now = datetime.now()


class FileSorter:
    def __init__(self, args) -> None:
        self.args = args

    def _move_file(self, dirpath, file, new_path):
        if (not dirpath.endswith("/")):
            full_path = f"{dirpath}/{file}"
        else:
            full_path = f"{dirpath}{file}"

        if (exists(f"{new_path}/{file}")):
            path = full_path.split(".")
            current_filename = path[-2:][0].split("/")[-1]
            new_filename = f"{current_filename}{now.strftime('%H%M%S%M')}"
            new_path = full_path.replace(current_filename, new_filename)

        shutil.move(full_path, new_path)

    def sort(self):
        for (dirpath, _, filenames) in walk(self.args.root_dir):
            for file in filenames:
                file_extension = file.split(".")[-1]
                if (file_extension.lower() in photo_extensions):
                    self._move_file(dirpath, file, self.args.photos_dir)
                elif (file_extension.lower() in video_extensions):
                    self._move_file(dirpath, file, self.args.videos_dir)
                elif (file_extension.lower() in doc_extensions):
                    self._move_file(dirpath, file, self.args.docs.dir)

def sort():
   fs =  FileSorter(parser.parse_args())
   fs.sort()

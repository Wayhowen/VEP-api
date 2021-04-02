import shutil
import zipfile
import os

from utils import get_uuid4


class Handler:
    def __init__(self):
        self._current_folders = set()

    def unzip_file(self, file_location):
        extraction_folder = self._create_extraction_folder(file_location)
        print(f"Extracting file to: {extraction_folder}")
        with zipfile.ZipFile(file_location) as zip_file:
            zip_file.extractall(extraction_folder)
        self._current_folders.add(extraction_folder)
        os.remove(file_location)
        return extraction_folder

    def _create_extraction_folder(self, file_location):
        extraction_folder = file_location.replace(".zip", f"_{get_uuid4()}")
        os.makedirs(extraction_folder)
        return extraction_folder

    def remove_folder(self, folder_to_remove):
        shutil.rmtree(folder_to_remove, ignore_errors=True)
        self._current_folders.remove(folder_to_remove)

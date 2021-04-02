import os
from collections import defaultdict

import settings


class Handler:
    def __init__(self, csv_handler):
        self.csv_handler = csv_handler

        self.metadata_file_name = "metadata.csv"
        self.file_pointers = settings.FILE_POINTERS

    def raw_activity_to_dict(self, activity_folder) -> dict:
        activity_dict = defaultdict(dict)
        metadata = self._read_metadata(activity_folder)

        for device, file_pointers in self.file_pointers.items():
            for file_pointer, func in file_pointers.items():
                if file_pointer in metadata:
                    file_location = os.path.join(activity_folder, metadata[file_pointer])
                    activity_dict[device][file_pointer] = self.csv_handler.read_file_contents(file_location,
                                                                                              func_to_apply=func)

        return activity_dict

    def _read_metadata(self, activity_folder):
        raw_metadata = self.csv_handler.read_file_contents(os.path.join(activity_folder,
                                                                        self.metadata_file_name))
        metadata = {item[0]: item[1] for item in raw_metadata[1:] if "INFO" not in item[0]}
        return metadata

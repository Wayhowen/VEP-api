import csv
import os
from datetime import datetime

import settings


class Reader:
    def __init__(self):
        self.data_folder = settings.DATA_FOLDER
        self.reader = csv.reader
        self.file_ending = ".csv"
        self.metadata_file_name = f"metadata{self.file_ending}"

        self.metadata = None

    def read_data(self):
        # files = [f for f in listdir(self.data_folder) if isfile(join(self.data_folder, f))]
        metadata = self._read_metadata()

        accelerometer_data = self._get_accelerometer_data(metadata)
        accelerometer_entry = self._get_accelerometer_entry(accelerometer_data)
        new_activity = Activity(name=metadata["activityName"],
                                start_time=datetime.fromtimestamp(int(metadata["startTimeStamp"])/1000),
                                finish_time=datetime.fromtimestamp(int(metadata["endTimeStamp"])/1000),
                                accelerometer_entry=accelerometer_entry,
                                patient_id=1
                                )
        new_activity.save()

    def _read_metadata(self):
        raw_metadata = self._read_file_contents(self.metadata_file_name)
        metadata = {item[0]: item[1] for item in raw_metadata[1:] if "INFO" not in item[0]}
        return metadata

    def _read_file_contents(self, filename, numerical=False, type=None):
        raw_csv_contents = []
        with open(os.path.join(self.data_folder, filename), "r") as csv_file:
            current_reader = self.reader(csv_file, delimiter=",")
            for row in current_reader:
                raw_csv_contents.append(row)
        if numerical:
            csv_contents = [type(item) for item in raw_csv_contents[0] if item]
            return csv_contents
        return raw_csv_contents

    def _get_accelerometer_data(self, metadata):
        raw_accelerometer_times = self._read_file_contents(metadata["ACCELEROMETER_TIMES"], numerical=True, type=int)
        accelerometer_times = [int(metadata["endTimeStamp"])/1000 - (time/1000) for time in reversed(raw_accelerometer_times)]
        accelerometer_x = self._read_file_contents(metadata["ACCELEROMETER_x"], numerical=True,
                                                   type=float)
        accelerometer_y = self._read_file_contents(metadata["ACCELEROMETER_y"], numerical=True,
                                                   type=float)
        accelerometer_z = self._read_file_contents(metadata["ACCELEROMETER_z"], numerical=True,
                                                   type=float)
        accelerometer_data = list(zip(accelerometer_times, accelerometer_x, accelerometer_y,
                                 accelerometer_z))
        return accelerometer_data

    def _get_accelerometer_entry(self, accelerometer_data):
        accelerometer_entry = AccelerometerEntry(actual_start_time=datetime.fromtimestamp(accelerometer_data[0][0]))
        accelerometer_entry.save()
        for data_point in accelerometer_data:
            AccelerometerData(time=datetime.fromtimestamp(data_point[0]), x=data_point[1],
                              y=data_point[2], z=data_point[3],
                              accelerometer_entry=accelerometer_entry).save()
        return accelerometer_entry

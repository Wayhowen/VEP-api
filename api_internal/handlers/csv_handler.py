import csv


class Handler:
    def __init__(self):
        self.reader = csv.reader

    def read_file_contents(self, csv_file_name, func_to_apply=None):
        raw_csv_contents = []
        with open(csv_file_name, "r") as csv_file:
            current_reader = self.reader(csv_file, delimiter=",")
            for row in current_reader:
                raw_csv_contents.append(row)
        if func_to_apply:
            csv_contents = [func_to_apply(item) for item in raw_csv_contents[0] if item]
            return csv_contents
        return raw_csv_contents

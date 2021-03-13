from data_processors.base_processor import BaseProcessor


class DataProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()

    def _preprocess_data(self, data):
        pass

    def _process_data(self, data):
        pass

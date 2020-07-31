class CSXExtractor:

    def __init__(self):
        pass

    def extract_textual_data(self, filepath):
        raise NotImplementedError('Extend me!')

    def batch_extract_textual_data(self, dirPath):
        raise NotImplementedError('Extend me!')

    def extract_figures(self, filepath):
        raise NotImplementedError('Extend me!')

    def batch_extract_figures(self, dirPath):
        raise NotImplementedError('Extend me!')
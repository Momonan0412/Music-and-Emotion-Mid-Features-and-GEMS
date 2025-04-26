import os

class DataAnnotator:
    def __init__(self, directory):
        self.__directory = directory
    
    def _find_files(self):
        for root, dirs, files in os.walk(self._get_dir()):
            for file in files:
                if file.endswith(".npy"):
                    print(file)
    
    def _get_dir(self):
        return self.__directory
    
    def _annotator(self):
        pass
    
    def _load_model(self):
        pass
    
    def _predictor(self):
        pass
    
if __name__ == "__main__":
    dir = "Emotify"
    da = DataAnnotator(dir)
    da._find_files()
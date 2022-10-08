from os.path import exists

class Io:
    def __init__(self) -> None:
        pass

    def open_file(self, file_path: str) -> str:
        if(not self.file_exist(file_path)):
            raise FileNotFoundError(f"Could not find file {file_path}")
        
        with open(file_path, 'r') as config:
            return config.read()
    
    def file_exist(self, file_path: str) -> bool:
        return exists(file_path)
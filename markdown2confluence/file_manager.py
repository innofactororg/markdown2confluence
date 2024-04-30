class FileManager:
    def read_file(self, path: str) -> str:
        """Read the content of a file."""
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

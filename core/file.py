from pathlib import Path

class File:
    def __init__(self, file_path: str):
        self.path = Path(file_path)
        self._exists()
        self._is_dir: bool = self.path.is_dir()

    def _exists(self):
        if not self.path.exists():
            raise FileNotFoundError(f"File {self.path} does not exist.")

    def _dir(self, _is: bool = True):
        if not self._is_dir and _is:
            raise IsADirectoryError(f"{self.path} is a directory.")

    def read(self) -> str:
        self._dir(False)
        return self.path.read_text(encoding="utf-8")

    def write(self, content: str):
        self._dir(False)
        self.path.write_text(content, encoding="utf-8")

    @property
    def dir(self):
        self._dir()
        for item in self.path.iterdir():
            if item.is_file():
                yield File(str(item))

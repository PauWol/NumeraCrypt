from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os
# Get the directory where this file resides.
base_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path)

def key_file_extension() -> str:
    env_path = os.getenv("KEY_FILE_EXTENSION")
    if not env_path:
        # Warn the user and use the current working directory as a fallback.
        import typer
        typer.echo("❗ Warning: KEY_FILE_EXTENSION is not set. Using the current default.")
        return ".nkey"
    return env_path


class File:
    def __init__(self, file_path: str):
        self.path = Path(file_path)
        self._is_dir: bool = self.path.is_dir()

    def _exists(self):
        if not self.path.exists():
            raise FileNotFoundError(f"File {self.path} does not exist.")

    def _dir(self, _is: bool = True):
        if not self._is_dir and _is:
            raise IsADirectoryError(f"{self.path} is a directory.")

    def read(self) -> str:
        self._exists()
        self._dir(False)
        return self.path.read_text(encoding="utf-8")

    def write(self, content: str):
        self._exists()
        self._dir(False)
        self.path.write_text(content, encoding="utf-8")

    @property
    def dir(self):
        self._exists()
        self._dir()
        for item in self.path.iterdir():
            if item.is_file():
                yield File(str(item))

    def key_store(self,key:str):
        """Store key in file"""
        if not self.path.exists():
            self.path.mkdir(parents=True)


        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        Path(self.path.resolve()).joinpath(f"key_{current_time}.{key_file_extension()}").write_text(key, encoding="utf-8")

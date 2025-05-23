from numeracrypt.core.convert import ASCII
from numeracrypt.core.file import File
from dotenv import load_dotenv
import random
import re
import os
# Get the directory where this file resides.
base_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path)

def key_store_location() -> str:
    env_path = os.getenv("KEY_STORAGE_DIRECTORY")
    if not env_path:
        # Warn the user and use the current working directory as a fallback.
        import typer
        typer.echo("❗ Warning: KEY_STORAGE_DIRECTORY is not set. Using the current working directory.")
        return os.getcwd()
    return os.path.expandvars(env_path)


class Key:
    def __init__(self, key: str = "", rounds: int = 5, max_length: int = 64):
        """
        If the provided key string contains a '/', it is assumed to be an already assembled key,
        and the salt is left empty. Otherwise, the provided key is used as the salt.
        """
        if rounds < 5:
            raise ValueError("Rounds must be at least 5 or more.")
        if max_length < 64:
            raise ValueError("Max length must be at least 64 or more.")

        self.rounds: int = rounds
        self.max_length: int = max_length

        # If key contains '/', treat it as a full key; otherwise, use it as the salt.
        if key and "/" in key:
            self.value: str = key
            self.salt: str = ""
        else:
            self.salt = key
            self.value = ""

    @staticmethod
    def extract_number_and_slash(text: str) -> str:
        """
        Extracts a number followed by a slash from the given text.
        For example, from '5/ABC' it returns '5'.
        """
        match = re.match(r'(\d+)/', text)
        return match.group(1) if match else None

    def _random_num(self) -> int:
        """
        Generates a random number of max_length digits and adds a salt-based offset.
        The salt is processed by summing the ASCII values of its characters.
        """
        salt_value = sum(ord(char) for char in self.salt) if self.salt else 0
        lower_bound = 10 ** (self.max_length - 1)
        upper_bound = 10 ** self.max_length - 1
        random_value = random.randint(lower_bound, upper_bound)
        salted_random_number = random_value + salt_value
        # Clamp the result to ensure it is still within the digit length.
        return min(max(salted_random_number, lower_bound), upper_bound)

    def _assemble_key(self, num: int) -> str:
        """
        Assembles the key using the rounds as prefix (with a slash) and the Base91-encoded number.
        """
        prefix = str(self.rounds) + "/"
        # Get the encoded key part from ASCII.
        key_part = ASCII(num).encode_base91()
        # Ensure key_part is a string (convert from bytes if needed)
        if isinstance(key_part, bytes):
            key_part = key_part.decode("utf-8")
        return prefix + key_part

    def generate(self) -> str:
        """
        Generates and a key.
        """
        num = self._random_num()
        self.value = self._assemble_key(num)
        return self.value

    def disassemble(self):
        """
        Disassembles the key into its Unicode-decoded number and the prefix (number of rounds).
        Returns a tuple (decoded_value, prefix).
        """
        if not self.value:
            raise ValueError("No key value available to disassemble.")
        prefix = self.extract_number_and_slash(self.value)
        if prefix is None:
            raise ValueError("Invalid key format; prefix missing.")
        # The rest of the key starts right after the prefix and the slash.
        rest = self.value[len(prefix) + 1:]
        decoded = ASCII(rest).ascii
        return decoded, int(prefix)

    def validate(self):
        """Checks if the key is valid."""
        if not self.value:
            return False
        _prefix = self.extract_number_and_slash(self.value)
        if _prefix is None or int(_prefix) <= 0:
            return False
        rest = self.value[len(_prefix) + 1:]
        if len(ASCII(rest).string) < self.max_length:
            return False
        return True

    def safe(self,path:str = None):
        """Safes the key to a file either using the provided path or the KEY_PATH environment variable."""
        if not self.value:
            raise ValueError("No key value available to safe.")

        if not self.validate():
            raise ValueError("Invalid key format. Please use a valid key.")

        if not path:
            path = key_store_location()
        File(path).key_store(self.value)




if __name__ == "__main__":
    # Generate a new key using an empty salt (or provide your custom salt here)
    key_generator = Key("my_secret_salt")
    assembled_key = key_generator.generate()
    print("Generated Key:", assembled_key)

    key_generator.safe()

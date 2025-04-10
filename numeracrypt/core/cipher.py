from numeracrypt.core.convert import ASCII
from numeracrypt.core.key import Key
from numeracrypt.core.file import File

class NumeraCrypt:
    def __init__(self, value: str, key: str, file: bool = False,dir: bool = False):
        """
        Initialize NumeraCrypt with either a plaintext or a file's content,
        plus a key (which will later be disassembled into its raw form and rounds).

        :param value: String content or file path.
        :param key: The key as a string.
        :param file: Flag indicating if 'value' should be read from a file.
        """
        self.file = file
        self.dir = dir
        if file:
            self.file_inst = File(value)
            self.value = ""
        elif dir:
            self.dir_inst = File(value)
            self.value = ""
        else:
            self.value = value

        self.key = Key(key)
        self.key_raw, self.rounds = self.key.disassemble()
        self.ascii_inst = ASCII(self.value)

    @staticmethod
    def compute_offset(round_num: int, key: int) -> int:
        """
        Compute a pseudo-random offset from the round number and key.

        Parameters:
            round_num (int): The round number (0, 1, 2, ...).
            key (int): The key (0-255).

        Returns:
            int: An offset value between 0 and 255.
        """
        # Multiplication and XOR, then mod 256 to ensure result is a byte.
        offset = ((round_num * (2 * key + 1)) ^ (round_num + key)) % 256
        return offset

    def _update_read(self):
        if self.file:
            self.value = self.file_inst.read()
            self.ascii_inst.value = self.value
        elif self.dir:
            self.value = self.dir_inst.read()
            self.ascii_inst.value = self.value

    def _value_check(self):
        if self.value == "":
            print("Error: Value is empty.")
            return False
        return True

    def encrypt_single(self, content: int, round_num: int, key: int) -> int:
        """
        Encrypt a single byte by offsetting its value.

        Parameters:
            content (int): The original byte (0-255).
            round_num (int): The current round number.
            key (int): The key byte (0-255) from key_raw.

        Returns:
            int: The encrypted byte (0-255).
        """
        offset = self.compute_offset(round_num, key)
        encrypted = (content + offset) % 256
        return encrypted

    def decrypt_single(self, encrypted: int, round_num: int, key: int) -> int:
        """
        Decrypt a single byte, reversing the offset.

        Parameters:
            encrypted (int): The encrypted byte (0-255).
            round_num (int): The same round number used in encryption.
            key (int): The key byte (0-255) from key_raw.

        Returns:
            int: The original content byte (0-255).
        """
        offset = self.compute_offset(round_num, key)
        original = (encrypted - offset) % 256
        return original

    def _key_part(self, index: int) -> int:
        """
        Retrieve the key component for the current position.
        Uses modulo arithmetic to wrap-around key_raw.

        :param index: Index of the byte being processed.
        :return: A key byte (0-255) from key_raw.
        """
        # Use modulo so that the key repeats cyclically.
        return self.key_raw[index % len(self.key_raw)]

    def _enc_round(self, round_c: int) -> list:
        """
        Perform one round of encryption on all content bytes.

        :param round_c: The current round number.
        :return: List of encrypted bytes.
        """
        # Process each byte with its corresponding key byte.
        return [
            self.encrypt_single(v, round_c, self._key_part(i))
            for i, v in enumerate(self.ascii_inst.ascii)
        ]

    def _dec_round(self, round_c: int) -> list:
        """
        Perform one round of decryption on all content bytes.

        :param round_c: The current round number.
        :return: List of decrypted bytes.
        """

        return [
            self.decrypt_single(v, round_c, self._key_part(i))
            for i, v in enumerate(self.ascii_inst.ascii)
        ]

    def _encrypt(self):
        """
        Encrypt the input content for the given number of rounds and return a Base91-encoded string.

        :return: The encrypted content as a Base91 string.
        """
        self._value_check()
        for round_c in range(self.rounds):
            # Update ascii_inst.value with the encrypted list (which is then interpreted as bytes later by ASCII)
            self.ascii_inst.value = self._enc_round(round_c)
        return self.ascii_inst.encode_base91()

    def encrypt(self):
        if self.file:
            self._update_read()
            self.file_inst.write(self._encrypt())
        elif self.dir:
            for file in self.dir_inst.dir:
                self.value = file.read()
                self.ascii_inst.value = self.value
                file.write(self._encrypt())
        else:
            return self._encrypt()

    def _decrypt(self):
        """
        Decrypt the encrypted content over the given number of rounds and return the decoded string.

        :return: The decrypted (original) content.
        """
        self._value_check()
        self.ascii_inst.value = self.ascii_inst.decode_base91()
        for round_c in range(self.rounds):
            self.ascii_inst.value = self._dec_round(round_c)
        return self.ascii_inst.string

    def decrypt(self):
        if self.file:
            self._update_read()
            self.file_inst.write(self._decrypt())
        elif self.dir:
            for file in self.dir_inst.dir:
                self.value = file.read()
                self.ascii_inst.value = self.value
                file.write(self._decrypt())
        else:
            return self._decrypt()


if __name__ == "__main__":
    import time
    text = "../test"
    #text = " Ih4nrv{fC"
    key = "5/[4*Ewn*zs17=mC%Shwx.3i*Xh2X<Ak$SjwlE[h+GR2D.@@bRX%VEcj:GB2U<pNmT3tlEKm<G[2,(pNH"

    nc = NumeraCrypt(text, key,file=False,dir=True)
    nc.encrypt()
    time.sleep(5)
    nc.decrypt()

import base91
from typing import Union, List


class ASCII:
    """
    Utility class to convert between integers, strings, and lists of ASCII values,
    and to encode/decode with Base91.

    Attributes:
        value (Union[int, str, List[int]]): The input data which can be:
            - An integer, representing a single ASCII code.
            - A string.
            - A list of integers representing ASCII codes.
    """

    def __init__(self, value: Union[int, str, List[int], bytes]) -> None:
        self.value: Union[int, str, List[int], bytes] = value

    @property
    def is_list(self) -> bool:
        """
        Determine if the internal value should be treated as a sequence
        (when it's a list or a string with more than one character).
        """
        return isinstance(self.value, list) or (isinstance(self.value, str) and len(self.value) > 1)

    @property
    def string(self) -> str:
        """
        Return the string representation of the stored value.
        If self.value is a list of integers, convert each ASCII code to character.
        """
        if isinstance(self.value, list):
            # Assume list contains integer ASCII codes.
            return "".join(chr(i) for i in self.value)
        elif isinstance(self.value, int):
            if not 0 <= self.value > 255:
                return chr(self.value)
            else:
                return str(self.value)

        elif isinstance(self.value, str):
            return self.value
        else:
            raise ValueError("Unsupported type for value")

    @property
    def ascii(self) -> Union[int, List[int]]:
        """
        Return the ASCII code(s) representation.
        If self.value is a string with one character, return the integer code.
        Otherwise, return a list of ASCII codes.
        """
        if isinstance(self.value, list):
            return [int(i) for i in self.value]
        elif isinstance(self.value, str):
            return [ord(c) for c in self.value] if len(self.value) > 1 else ord(self.value)
        elif isinstance(self.value, int):
            return self.value
        else:
            raise ValueError("Unsupported type for value")

    def encode_base91(self) -> str:
        """
        Encode the string representation of self.value into Base91 format.
        """
        return base91.encode(self.string.encode("utf-8"))

    def decode_base91(self) -> str:
        """
        Decode self.value from Base91. Assumes self.value is the Base91 encoded string.
        """
        # Here we use self.string as the input Base91 string.
        return base91.decode(self.string).decode("utf-8")


# Example usage:
if __name__ == "__main__":
    # Display single character conversion.
    text = ("qskdivsivfvsbgrbsngbrgb" +
            "wwwwweeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    ascii_single = ASCII(65)
    print("ASCII(65).string:", ascii_single.string)  # 'A'

    # Conversion of a string to ASCII codes.
    ascii_str = ASCII(text)
    print("ASCII('Abcd').ascii_codes:", ascii_str.ascii)  # [65, 98, 99, 100]

    # Using Base91: encode a long text.

    # First convert text to its ASCII code representation and reinitialize.
    ascii_text = ASCII(text)
    encoded = ascii_text.encode_base91()

    print("Base91 Encoded:", encoded, "Length:", len(encoded))
    print("Original text length:", len(text))
    print("Length difference:", len(encoded) - len(text))

    # To decode a Base91 encoded string (make sure the value is the encoded one):
    encoded_instance = ASCII(encoded)
    decoded_text = encoded_instance.decode_base91()
    print("Decoded:", decoded_text)

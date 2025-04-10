from numeracrypt.core.cipher import NumeraCrypt
from numeracrypt.core.key import Key

text = "Hello, secure world!"

key = Key("your_secret_salt",rounds=7,max_length=64)
your_key = key.generate()

nc = NumeraCrypt(value=text, key=your_key)
encrypted = nc.encrypt()
print("Encrypted:", encrypted)

nc_decrypt = NumeraCrypt(value=encrypted, key=your_key)
decrypted = nc_decrypt.decrypt()
print("Decrypted:", decrypted)
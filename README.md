# 🔐 NumeraCrypt

NumeraCrypt is a custom byte-level encryption algorithm that performs multiple rounds of transformation using a key-derived offset system. It includes optional file and directory processing, and the final result is Base91-encoded for compact encrypted output.

⚠️ **Early Stage Warning:**\
This project is in an experimental and early development stage. It is not audited or guaranteed to be secure for production use. It was built for learning, research, and exploring custom encryption techniques.

---

## ✨ Features

- 🔢 Multi-round byte-level encryption
- 🔑 Custom key transformation logic
- 📂 Support for encrypting/decrypting:
  - Plaintext strings
  - Files
  - Entire directories of files
- 📦 Output encoded in Base91 for compact representation
- 🔄 Decryption reverses the entire pipeline

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or newer

### Installation

Clone the repository:

```bash
git clone https://github.com/pauwol/NumeraCrypt.git
cd NumeraCrypt
```

### Basic Usage

```python
from numeracrypt.core.cipher import NumeraCrypt
from numeracrypt.core.key import Key

text = "Hello, secure world!"

key = Key("your_secret_salt", rounds=7, max_length=64)
your_key = key.generate()

nc = NumeraCrypt(value=text, key=your_key)
encrypted = nc.encrypt()
print("Encrypted:", encrypted)

nc_decrypt = NumeraCrypt(value=encrypted, key=your_key)
decrypted = nc_decrypt.decrypt()
print("Decrypted:", decrypted)
```

### Encrypt a File

```python
nc = NumeraCrypt("path/to/file.txt", your_key, file=True)
nc.encrypt()
```

### Encrypt All Files in a Directory

```python
nc = NumeraCrypt("path/to/folder", your_key, dir=True)
nc.encrypt()
```

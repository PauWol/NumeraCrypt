import typer
from numeracrypt.core.cipher import NumeraCrypt
from numeracrypt.core.key import Key
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

def key_store_location() -> str:
    env_path = os.getenv("KEY_STORAGE_DIRECTORY", "key_storage")
    return os.path.expandvars(env_path)

app = typer.Typer(help="NumeraCrypt: A custom encryption tool.")

def validate_single_source(*sources):
    """Ensure that exactly one source (content, file, dir) is provided."""
    provided = [s for s in sources if s is not None]
    if len(provided) == 0:
        typer.echo("❗ Error: Please specify exactly one of --content, --file, or --dir.")
        raise typer.Exit(1)
    if len(provided) > 1:
        typer.echo("❗ Error: Please provide only one of --content, --file, or --dir at a time.")
        raise typer.Exit(1)

@app.command()
def encrypt(
    content: str = typer.Option(None, help="Content to encrypt."),
    file: Path = typer.Option(None, exists=True, help="Path to the file to encrypt."),
    dir: Path = typer.Option(None, exists=True, help="Path to the directory to encrypt."),
    key: str = typer.Option(None, help="Encryption key. If not provided, one will be generated."),
    keysafe: bool = typer.Option(False, help="Flag to save the encryption key to a file."),
    contentsafe: bool = typer.Option(False, help="Flag to save the encrypted content to a file.")
):
    """Encrypt files, directories, or strings using NumeraCrypt."""
    # Ensure exactly one source is provided.
    validate_single_source(content, file, dir)

    # Generate a key if one wasn't provided.
    if not key:
        key = Key(rounds=8, max_length=64).generate()
        typer.echo(f"🔑 Generated key: {key}")

    # Validate the provided (or generated) key.
    if not Key(key).validate():
        typer.echo("❗ Invalid key format. Please use a valid key.")
        raise typer.Exit(1)

    encrypted_result = None
    if content:
        nc = NumeraCrypt(str(content), key)
        encrypted_result = nc.encrypt()
        typer.echo(f"🔒 Encrypted content: {encrypted_result}")
    elif file:
        nc = NumeraCrypt(str(file), key, file=True)
        nc.encrypt()
        typer.echo(f"🔒 Encrypted file: {file}")
    elif dir:
        nc = NumeraCrypt(str(dir), key, dir=True)
        nc.encrypt()
        typer.echo(f"🔒 Encrypted directory: {dir}")

    if keysafe:
        Key(key).safe()
        typer.echo(f"📄 Key saved to {key_store_location()}")

    if contentsafe:
        # Only applicable for string encryption.
        if encrypted_result is not None:
            result_path = Path("encrypted_content.txt")
            result_path.write_text(encrypted_result)
            typer.echo(f"📄 Encrypted content saved to {result_path}")
        else:
            typer.echo("❗ Encrypted content saving is only available for string encryption.")

@app.command()
def decrypt(
    content: str = typer.Option(None, help="Content to decrypt."),
    file: Path = typer.Option(None, exists=True, help="Path to the file to decrypt."),
    dir: Path = typer.Option(None, exists=True, help="Path to the directory to decrypt."),
    key: str = typer.Option(None, help="Decryption key."),
    keysafe: bool = typer.Option(False, help="Flag to save the decryption key to a file."),
    contentsafe: bool = typer.Option(False, help="Flag to save the decrypted content to a file.")
):
    """Decrypt files, directories, or strings using NumeraCrypt."""
    # Validate that a source is provided before doing any further processing.
    if not (content or file or dir):
        typer.echo("❗ Error: Please specify at least one of --content, --file, or --dir.")
        raise typer.Exit(1)

    # Now, if key wasn't provided, prompt the user.
    if not key:
        key = typer.prompt("Please enter the decryption key")

    if not Key(key).validate():
        typer.echo("❗ Invalid key format. Please use a valid key.")
        raise typer.Exit(1)

    decrypted_result = None
    if content:
        nc = NumeraCrypt(str(content), key)
        decrypted_result = nc.decrypt()
        typer.echo(f"🔓 Decrypted content: {decrypted_result}")
    elif file:
        nc = NumeraCrypt(str(file), key, file=True)
        nc.decrypt()
        typer.echo(f"🔓 Decrypted file: {file}")
    elif dir:
        nc = NumeraCrypt(str(dir), key, dir=True)
        nc.decrypt()
        typer.echo(f"🔓 Decrypted directory: {dir}")

    if keysafe:
        Key(key).safe()
        typer.echo(f"📄 Key saved to {key_store_location()}")

    if contentsafe:
        # Only applicable when decrypting content.
        if decrypted_result is not None:
            result_path = Path("decrypted_content.txt")
            result_path.write_text(decrypted_result)
            typer.echo(f"📄 Decrypted content saved to {result_path}")
        else:
            typer.echo("❗ Decrypted content saving is only available for string decryption.")

@app.command()
def key(
    key: str = typer.Option(None, help="Key to validate."),
    salt: str = typer.Option(None, help="Salt to generate a key from."),
    rounds: int = typer.Option(8, help="Number of rounds to use for encryption (min 5)."),
    length: int = typer.Option(64, help="Length of the key (min 64)."),
    keysafe: bool = typer.Option(False, help="Flag to save the generated key to a file.")
):
    """Generate a key or validate an existing one."""
    if rounds < 5:
        typer.echo("❗ Number of rounds must be at least 5.")
        raise typer.Exit(1)
    if length < 64:
        typer.echo("❗ Key length must be at least 64.")
        raise typer.Exit(1)

    if key:
        if not Key(key).validate():
            typer.echo("❗ Invalid key format.")
            raise typer.Exit(1)
        typer.echo("✅ Key is valid.")
    elif salt:
        key_generator = Key(salt, rounds, length)
        key = key_generator.generate()
        typer.echo(f"🔑 Generated key from salt: {key}")
    else:
        key_generator = Key("", rounds, length)
        key = key_generator.generate()
        typer.echo(f"🔑 Generated key: {key}")

    if keysafe:
        key_generator.safe()
        typer.echo(f"📄 Key saved to {key_store_location()}")

if __name__ == "__main__":
    app()

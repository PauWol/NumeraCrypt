import typer
from numeracrypt.core.cipher import NumeraCrypt
from numeracrypt.core.key import Key
from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()

def key_store_location() -> str:
    env_path = os.getenv("KEY_STORAGE_DIRECTORY")
    return os.path.expandvars(env_path)

app = typer.Typer(help="NumeraCrypt: A custom encryption tool.")

@app.command()
def encrypt(
    content: str = typer.Option(None, help="Content to encrypt."),
    file: Path = typer.Option(None, exists=True, help="Path to the file to encrypt."),
    dir: Path = typer.Option(None, exists=True, help="Path to the directory to encrypt."),
    key: str = typer.Option(None, help="Encryption key. If not provided, one will be generated."),
    key_safe: bool = typer.Option(False, help="Flag to save the encryption key to a file."),
    content_safe: bool = typer.Option(False, help="Flag to save the encrypted content to a file.")
):
    """Encrypt files, directories, or strings using NumeraCrypt."""
    # Generate key if not provided
    if not file or not dir or not content:
        typer.echo("❗ Please specify a file, a directory, or content to encrypt.")
        raise typer.Exit(1)

    if not key:
        key = Key(rounds=8, max_length=64).generate()
        typer.echo(f"🔑 Generated key: {key}")

    if not Key(key).validate():
        typer.echo("❗ Invalid key format. Please use a valid key.")
        raise typer.Exit(1)

    if file:
        nc = NumeraCrypt(str(file), key, file=True)
        nc.encrypt()
        typer.echo(f"🔒 Encrypted file: {file}")
    elif dir:
        nc = NumeraCrypt(str(dir), key, dir=True)
        nc.encrypt()
        typer.echo(f"🔒 Encrypted directory: {dir}")
    elif content:
        nc = NumeraCrypt(str(content), key)
        encrypted_content = nc.encrypt()
        typer.echo(f"🔒 Encrypted content: {encrypted_content}")

    if key_safe:
        Key(key).safe()
        typer.echo(f"📄  Key saved to {key_store_location()}")

    if content_safe:
        encrypted_path = Path("encrypted_content.txt")
        encrypted_path.write_text(encrypted_content)
        typer.echo(f"📄 Encrypted content saved to {encrypted_path}")


@app.command()
def decrypt(
    content: str = typer.Option(None, help="Content to decrypt."),
    file: Path = typer.Option(None, exists=True, help="Path to the file to decrypt."),
    dir: Path = typer.Option(None, exists=True, help="Path to the directory to decrypt."),
    key: str = typer.Option(
        None,            # Default is None so that if not provided, it prompts.
        help="Decryption key.",
        prompt="Please enter the decryption key:"  # This is the prompt message.
    ),
    keysafe: bool = typer.Option(False, help="Flag to save the decryption key to a file."),
    contentsafe: bool = typer.Option(False, help="Flag to save the decrypted content to a file.")
):
    """Decrypt files or directories using NumeraCrypt."""
    if not file and not dir and not content:
        typer.echo("❗ Please specify a file, a directory, or content to decrypt.")
        raise typer.Exit(1)

    if not Key(key).validate():
        typer.echo("❗ Invalid key format. Please use a valid key.")
        raise typer.Exit(1)

    if content:
        nc = NumeraCrypt(str(content), key)
        typer.echo(f"🔓 Decrypted content: {nc.decrypt()}")
    elif file:
        nc = NumeraCrypt(str(file), key, file=True)
        nc.decrypt()
        typer.echo(f"🔓 Decrypted file: {file}")
    elif dir:
        nc = NumeraCrypt(str(dir), key, dir=True)
        nc.decrypt()
        typer.echo(f"🔓 Decrypted directory: {dir}")
    else:
        typer.echo("❗ Please specify a file or directory to decrypt.")
        raise typer.Exit(1)

    if keysafe:
        Key(key).safe()
        typer.echo(f"📄  Key saved to {key_store_location()}")

    if contentsafe:
        decrypted_path = Path("decrypted_content.txt")
        decrypted_path.write_text(nc.ascii_inst.string)
        typer.echo(f"📄 Decrypted content saved to {decrypted_path}")

@app.command()
def key(
    key: str = typer.Option(None, help="Key to validate."),
    salt: str = typer.Option(None, help="Salt to generate a key from."),
    rounds: int = typer.Option(8, help="Number of rounds to use for later encryption."),
    length: int = typer.Option(64, help="Length of the key."),
    key_safe: bool = typer.Option(False, help="Flag to save the generated key to a file.")
):
    """Generate a key or validate an existing one."""

    if rounds:
        if rounds < 5:
            typer.echo("❗ Number of rounds must be at least 5.")
            raise typer.Exit(1)

    if length:
        if length < 64:
            typer.echo("❗ Key length must be at least 64.")
            raise typer.Exit(1)

    if key:
        if not Key(key).validate():
            typer.echo("❗ Invalid key format.")
            raise typer.Exit(1)
        typer.echo("✅  Key is valid.")
    elif salt:
        key_generator = Key(salt, rounds, length)
        key = key_generator.generate()
        typer.echo(f"🔑 Generated key: {key}")
    else:
       key_generator = Key("", rounds, length)
       key = key_generator.generate()
       typer.echo(f"🔑 Generated key: {key}")

    if key_safe:
        key_generator.safe()
        typer.echo(f"📄  Key saved to { key_store_location() }")

if __name__ == "__main__":
    app()

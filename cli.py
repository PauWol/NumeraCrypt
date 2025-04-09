import typer
from core.cipher import NumeraCrypt
from core.key import Key
from pathlib import Path

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
    else:
        typer.echo("❗ Please specify a file, a directory, or content to encrypt.")
        raise typer.Exit(1)

    if key_safe:
        key_path = Path("encryption_key.txt")
        key_path.write_text(key)
        typer.echo(f"📄  Key saved to {key_path}")

    if content_safe:
        encrypted_path = Path("encrypted_content.txt")
        encrypted_path.write_text(encrypted_content)
        typer.echo(f"📄 Encrypted content saved to {encrypted_path}")


@app.command()
def decrypt(
    file: Path = typer.Option(None, exists=True, help="Path to the file to decrypt."),
    dir: Path = typer.Option(None, exists=True, help="Path to the directory to decrypt."),
    key: str = typer.Option(..., help="Decryption key."),
    keysafe: bool = typer.Option(False, help="Flag to save the decryption key to a file."),
    contentsafe: bool = typer.Option(False, help="Flag to save the decrypted content to a file.")
):
    """Decrypt files or directories using NumeraCrypt."""
    if not Key(key).validate():
        typer.echo("❗ Invalid key format. Please use a valid key.")
        raise typer.Exit(1)

    if file:
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
        key_path = Path("decryption_key.txt")
        key_path.write_text(key)
        typer.echo(f"📄  Key saved to {key_path}")

    if contentsafe:
        decrypted_path = Path("decrypted_content.txt")
        decrypted_path.write_text(nc.ascii_inst.string)
        typer.echo(f"📄 Decrypted content saved to {decrypted_path}")


if __name__ == "__main__":
    app()

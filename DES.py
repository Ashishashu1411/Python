import sys
import base64
from Crypto.Cipher import DES

BLOCK_SIZE = 8  # DES block size in bytes


def _make_key(key_str: str) -> bytes:
        b = key_str.encode("utf-8")
        if len(b) >= BLOCK_SIZE:
                return b[:BLOCK_SIZE]
        return b.ljust(BLOCK_SIZE, b"\0")


def pkcs5_pad(data: bytes) -> bytes:
        pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
        return data + bytes([pad_len]) * pad_len


def pkcs5_unpad(data: bytes) -> bytes:
        if not data or len(data) % BLOCK_SIZE != 0:
                raise ValueError("Invalid padded data length")
        pad_len = data[-1]
        if pad_len < 1 or pad_len > BLOCK_SIZE:
                raise ValueError("Invalid padding")
        if data[-pad_len:] != bytes([pad_len]) * pad_len:
                raise ValueError("Invalid padding bytes")
        return data[:-pad_len]


def encrypt(plaintext: str, key: bytes) -> str:
        cipher = DES.new(key, DES.MODE_ECB)
        pt_bytes = plaintext.encode("utf-8")
        ct = cipher.encrypt(pkcs5_pad(pt_bytes))
        return base64.b64encode(ct).decode("ascii")


def decrypt(b64_ciphertext: str, key: bytes) -> str:
        try:
                ct = base64.b64decode(b64_ciphertext)
        except Exception:
                raise ValueError("Ciphertext is not valid base64")
        cipher = DES.new(key, DES.MODE_ECB)
        pt_padded = cipher.decrypt(ct)
        pt = pkcs5_unpad(pt_padded)
        return pt.decode("utf-8", errors="replace")


def prompt(prompt_text: str) -> str:
        try:
                return input(prompt_text)
        except EOFError:
                print()
                sys.exit(0)


def main():
        print("DES encrypt/decrypt (ECB mode, PKCS#5 padding)")
        key_str = prompt("Enter key (8 chars recommended): ")
        key = _make_key(key_str)

        mode = prompt("Choose mode - (E)ncrypt or (D)ecrypt: ").strip().lower()
        if mode.startswith("e"):
                plaintext = prompt("Enter plaintext to encrypt: ")
                try:
                        ciphertext_b64 = encrypt(plaintext, key)
                        print("\nCiphertext (base64):")
                        print(ciphertext_b64)
                except Exception as ex:
                        print("Encryption error:", ex)
        elif mode.startswith("d"):
                ciphertext_b64 = prompt("Enter base64 ciphertext to decrypt: ")
                try:
                        plaintext = decrypt(ciphertext_b64.strip(), key)
                        print("\nDecrypted plaintext:")
                        print(plaintext)
                except Exception as ex:
                        print("Decryption error:", ex)
        else:
                print("Unknown mode. Choose E or D.")


if __name__ == "__main__":
        main()
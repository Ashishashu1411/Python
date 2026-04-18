from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import os

# Function to generate and save RSA key pair
def generate_keys():
    key_pair = RSA.generate(2048)
    private_key = key_pair.export_key()
    public_key = key_pair.publickey().export_key()

    with open("private.pem", "wb") as f:
        f.write(private_key)
    with open("public.pem", "wb") as f:
        f.write(public_key)

    print("\n Keys generated and saved as 'private.pem' and 'public.pem'\n")

# Function to load keys
def load_keys():
    if not (os.path.exists("private.pem") and os.path.exists("public.pem")):
        generate_keys()
    with open("private.pem", "rb") as f:
        private_key = RSA.import_key(f.read())
    with open("public.pem", "rb") as f:
        public_key = RSA.import_key(f.read())
    return private_key, public_key

# Load existing keys or generate new ones
private_key, public_key = load_keys()
encryptor = PKCS1_OAEP.new(public_key)
decryptor = PKCS1_OAEP.new(private_key)

# Menu
choice = input("Do you want to Encrypt or Decrypt? (E/D): ").strip().upper()

if choice == "E":
    plaintext = input("Enter plaintext: ").encode()
    encrypted = encryptor.encrypt(plaintext)
    hex_encrypted = binascii.hexlify(encrypted).decode()
    print("\nEncrypted (Hex):", hex_encrypted)

elif choice == "D":
    cipher_text = input("Enter ciphertext (Hex): ").strip().replace(" ", "").replace("\n", "")

    # Check if length is even
    if len(cipher_text) % 2 != 0:
        print(" Error: Ciphertext has odd length! Please ensure it's a valid hex string.")
    else:
        try:
            encrypted_bytes = binascii.unhexlify(cipher_text)
            decrypted = decryptor.decrypt(encrypted_bytes)
            print("\n Decrypted Text:", decrypted.decode())
        except Exception as e:
            print(f" Decryption failed: {e}")
else:
    print(" Invalid choice! Please enter 'E' for Encrypt or 'D' for Decrypt.")

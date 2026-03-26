from Crypto.Cipher import AES
import binascii

# Padding function (AES block size = 16 bytes)
def pad(text):
    while len(text) % 16 != 0:
        text += ' '
    return text

# Encryption
def aes_encrypt(plain_text, key):
    cipher = AES.new(key, AES.MODE_ECB)   # Using ECB mode for simplicity
    padded_text = pad(plain_text)
    encrypted_bytes = cipher.encrypt(padded_text.encode())
    return binascii.hexlify(encrypted_bytes).decode()

# Decryption
def aes_decrypt(cipher_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_bytes = cipher.decrypt(binascii.unhexlify(cipher_text))
    return decrypted_bytes.decode().rstrip()

# Main Program
if __name__ == "__main__":
    choice = input("Do you want to Encrypt or Decrypt? (E/D): ").strip().upper()
    key_input = input("Enter a key (16/24/32 characters for AES-128/192/256): ")

    # Convert key to bytes
    key = key_input.encode()

    if len(key) not in [16, 24, 32]:
        print("Error: Key length must be 16, 24, or 32 characters!")
    else:
        if choice == "E":
            text = input("Enter plaintext: ")
            cipher = aes_encrypt(text, key)
            print("Encrypted (Hex):", cipher)

        elif choice == "D":
            cipher_text = input("Enter ciphertext (Hex): ")
            decrypted = aes_decrypt(cipher_text, key)
            print("Decrypted Text:", decrypted)

        else:
            print("Invalid choice! Please enter E for Encrypt or D for Decrypt.")

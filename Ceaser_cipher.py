def encrypt(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            shift = 65 if char.isupper() else 97
            result += chr((ord(char) - shift + key) % 26 + shift)
        else:
            result += char
    return result

def decrypt(text, key):
    return encrypt(text, -key)

# Example
plaintext = "HELLO"
key = 3
encrypted = encrypt(plaintext, key)
decrypted = decrypt(encrypted, key)
print("Plaintext:", plaintext)
print("Key:", key)
print("Encrypted Text:", encrypted)
print("Decrypted Text:", decrypted)
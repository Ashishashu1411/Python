# XOR Encryption and Decryption Program

def xor_encrypt_decrypt(text, key):
    result = ""
    for i in range(len(text)):
        result += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return result


print("------ XOR Cipher ------")
choice = input("Do you want to Encrypt or Decrypt? (E/D): ").upper()

text = input("Enter your text: ")
key = input("Enter key: ")

if choice == 'E':
    encrypted = xor_encrypt_decrypt(text, key)
    # Convert encrypted data to hex for better readability
    hex_output = encrypted.encode("utf-8").hex()
    print("\nEncrypted Text (Hex):", hex_output)

elif choice == 'D':
    try:
        # Decrypt from hex input
        hex_data = bytes.fromhex(text).decode("utf-8", errors='ignore')
        decrypted = xor_encrypt_decrypt(hex_data, key)
        print("\nDecrypted Text:", decrypted)
    except Exception as e:
        print("Error: Make sure you entered the correct hex ciphertext.")

else:
    print("Invalid choice! Please enter E or D.")
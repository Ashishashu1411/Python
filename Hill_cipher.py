import numpy as np

# Function to convert text to numbers (A=0, B=1, ..., Z=25)
def text_to_numbers(text):
    return [ord(c) - 65 for c in text.upper().replace(" ", "")]

# Function to convert numbers back to text
def numbers_to_text(numbers):
    return "".join([chr(n % 26 + 65) for n in numbers])

# Hill Cipher Encryption
def hill_encrypt(plaintext, key_matrix):
    n = key_matrix.shape[0]
    plaintext_numbers = text_to_numbers(plaintext)

    # Padding if not divisible by n
    while len(plaintext_numbers) % n != 0:
        plaintext_numbers.append(23)  # pad with 'X'

    plaintext_matrix = np.array(plaintext_numbers).reshape(-1, n)
    cipher_matrix = (plaintext_matrix.dot(key_matrix)) % 26
    cipher_text = numbers_to_text(cipher_matrix.flatten())
    return cipher_text

# Hill Cipher Decryption
def hill_decrypt(ciphertext, key_matrix):
    n = key_matrix.shape[0]

    # Find modular inverse of determinant
    det = int(round(np.linalg.det(key_matrix))) % 26
    det_inv = pow(det, -1, 26)

    # Find adjoint (matrix of cofactors, transposed)
    key_inv = (
        det_inv * np.round(det * np.linalg.inv(key_matrix)).astype(int)
    ) % 26

    ciphertext_numbers = text_to_numbers(ciphertext)
    ciphertext_matrix = np.array(ciphertext_numbers).reshape(-1, n)

    decrypted_matrix = (ciphertext_matrix.dot(key_inv)) % 26
    decrypted_text = numbers_to_text(decrypted_matrix.flatten())
    return decrypted_text

# Main program
if __name__ == "__main__":
    print("------ Hill Cipher ------")
    choice = input("Enter 'E' for Encryption or 'D' for Decryption: ").upper()

    n = int(input("Enter size of key matrix (n): "))
    print("Enter key matrix row by row (space separated):")

    key_matrix = []
    for i in range(n):
        row = list(map(int, input().split()))
        key_matrix.append(row)

    key_matrix = np.array(key_matrix)

    if choice == "E":
        plaintext = input("Enter plaintext (A-Z only): ")
        cipher_text = hill_encrypt(plaintext, key_matrix)
        print("\nEncrypted Text:", cipher_text)

    elif choice == "D":
        ciphertext = input("Enter ciphertext (A-Z only): ")
        plain_text = hill_decrypt(ciphertext, key_matrix)
        print("\nDecrypted Text:", plain_text)
    else:
        print("Invalid choice!")
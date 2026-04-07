# Playfair Cipher Implementation (Encryption + Decryption)

def generate_matrix(key):
    key = key.upper().replace("J", "I")  # J ko I se replace karte hain
    matrix = []
    used = set()
    
    for char in key:
        if char not in used and char.isalpha():
            matrix.append(char)
            used.add(char)
    
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # J already replaced
        if char not in used:
            matrix.append(char)
            used.add(char)
    
    # 5x5 matrix
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None

def process_text(text):
    text = text.upper().replace("J", "I")
    result = ""
    i = 0
    while i < len(text):
        a = text[i]
        if not a.isalpha():
            i += 1
            continue
        if i+1 < len(text):
            b = text[i+1]
            if not b.isalpha():
                result += a
                i += 1
                continue
            if a == b:  # same letters
                result += a + "X"
                i += 1
            else:
                result += a + b
                i += 2
        else:
            result += a + "X"
            i += 1
    return result

def encrypt_pair(pair, matrix):
    r1, c1 = find_position(matrix, pair[0])
    r2, c2 = find_position(matrix, pair[1])
    
    if r1 == r2:  # same row
        return matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
    elif c1 == c2:  # same column
        return matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
    else:  # rectangle case
        return matrix[r1][c2] + matrix[r2][c1]

def decrypt_pair(pair, matrix):
    r1, c1 = find_position(matrix, pair[0])
    r2, c2 = find_position(matrix, pair[1])
    
    if r1 == r2:  # same row
        return matrix[r1][(c1-1)%5] + matrix[r2][(c2-1)%5]
    elif c1 == c2:  # same column
        return matrix[(r1-1)%5][c1] + matrix[(r2-1)%5][c2]
    else:  # rectangle case
        return matrix[r1][c2] + matrix[r2][c1]

def encrypt(text, key):
    matrix = generate_matrix(key)
    text = process_text(text)
    ciphertext = ""
    for i in range(0, len(text), 2):
        ciphertext += encrypt_pair(text[i:i+2], matrix)
    return ciphertext

def decrypt(ciphertext, key):
    matrix = generate_matrix(key)
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        plaintext += decrypt_pair(ciphertext[i:i+2], matrix)
    return plaintext
key = input("Enter Key: ")
text = input("Enter Text: ")

encrypted = encrypt(text, key)
decrypted = decrypt(encrypted, key)

print("Key Matrix:")
for row in generate_matrix(key):
    print(row)

print("\nPlaintext:", text)
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)
import sys
import math
import re

def sanitize(text):
    return re.sub(r'[^A-Z0-9]', '', text.upper())

def key_order(key):
    k = [c for c in key]
    indexed = list(enumerate(k))
    # sort by char then by original index to break ties deterministically
    sorted_indexed = sorted(indexed, key=lambda x: (x[1], x[0]))
    # return list of original indices in sorted order
    return [orig_idx for orig_idx, _ in sorted_indexed]

def encrypt(plaintext, key, pad_char='X'):
    pt = sanitize(plaintext)
    if not pt:
        return ''
    cols = len(key)
    # pad to full rectangle
    pad_len = (cols - (len(pt) % cols)) % cols
    pt += pad_char * pad_len
    rows = len(pt) // cols
    # build matrix row-wise
    matrix = [list(pt[r*cols:(r+1)*cols]) for r in range(rows)]
    order = key_order(key)
    # read columns in key order
    ciphertext = []
    for col_idx in order:
        for r in range(rows):
            ciphertext.append(matrix[r][col_idx])
    return ''.join(ciphertext)

def decrypt(ciphertext, key):
    ct = sanitize(ciphertext)
    if not ct:
        return ''
    cols = len(key)
    rows = len(ct) // cols
    if rows * cols != len(ct):
        raise ValueError("Ciphertext length must be multiple of key length (encryption pads to rectangle).")
    order = key_order(key)
    # prepare empty matrix
    matrix = [[''] * cols for _ in range(rows)]
    pos = 0
    # fill columns in key order with slices of ciphertext
    for col_idx in order:
        for r in range(rows):
            matrix[r][col_idx] = ct[pos]
            pos += 1
    # read row-wise
    plaintext = ''.join(''.join(row) for row in matrix)
    # strip trailing pad characters (commonly 'X')
    return plaintext.rstrip('X')

def prompt_loop():
    try:
        while True:
            mode = input("Choose mode ([E]ncrypt / [D]ecrypt / [Q]uit): ").strip().upper()
            if mode == 'Q':
                print("Goodbye.")
                return
            if mode not in ('E', 'D'):
                print("Enter E, D, or Q.")
                continue
            text = input("Enter text: ")
            key = input("Enter key (letters/digits, at least 2 chars): ").strip().upper()
            if len(key) < 2:
                print("Key too short.")
                continue
            # keep only alphanumeric chars in key
            key = re.sub(r'[^A-Z0-9]', '', key)
            if not key:
                print("Invalid key.")
                continue
            try:
                if mode == 'E':
                    result = encrypt(text, key)
                    print("Ciphertext:", result)
                else:
                    result = decrypt(text, key)
                    print("Plaintext (decrypted):", result)
            except Exception as e:
                print("Error:", e)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")

if __name__ == '__main__':
    prompt_loop()
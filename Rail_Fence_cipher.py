# Lab5.py - Rail Fence Cipher (encryption & decryption)
# GitHub Copilot

def encrypt_rail_fence(plaintext: str, rails: int) -> str:
    if rails <= 1 or rails >= len(plaintext):
        return plaintext
    rows = [''] * rails
    r = 0
    step = 1
    for ch in plaintext:
        rows[r] += ch
        r += step
        if r == 0 or r == rails - 1:
            step = -step
    return ''.join(rows)

def decrypt_rail_fence(ciphertext: str, rails: int) -> str:
    if rails <= 1 or rails >= len(ciphertext):
        return ciphertext
    n = len(ciphertext)
    # mark pattern
    pattern = [[False] * n for _ in range(rails)]
    r = 0
    step = 1
    for i in range(n):
        pattern[r][i] = True
        r += step
        if r == 0 or r == rails - 1:
            step = -step
    # fill pattern with ciphertext chars row-wise
    idx = 0
    grid = [[''] * n for _ in range(rails)]
    for row in range(rails):
        for col in range(n):
            if pattern[row][col]:
                grid[row][col] = ciphertext[idx]
                idx += 1
    # read off in zig-zag order
    result_chars = []
    r = 0
    step = 1
    for i in range(n):
        result_chars.append(grid[r][i])
        r += step
        if r == 0 or r == rails - 1:
            step = -step
    return ''.join(result_chars)

def get_int(prompt: str) -> int:
    while True:
        try:
            v = int(input(prompt).strip())
            if v < 1:
                print("Please enter an integer >= 1.")
                continue
            return v
        except ValueError:
            print("Please enter a valid integer.")

def main():
    print("Rail Fence Cipher")
    choice = input("Choose (E)ncrypt or (D)ecrypt: ").strip().lower()
    if choice not in ('e', 'encrypt', 'd', 'decrypt'):
        print("Unknown choice. Use E or D.")
        return
    text = input("Enter the message: ")
    rails = get_int("Enter number of rails: ")
    if choice[0] == 'e':
        out = encrypt_rail_fence(text, rails)
        print("Encrypted:", out)
    else:
        out = decrypt_rail_fence(text, rails)
        print("Decrypted:", out)

if __name__ == "__main__":
    main()
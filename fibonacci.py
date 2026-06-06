def fibonacci(n):
    fib = [1, 1]
    while len(fib) < n:
        fib.append(fib[-1] + fib[-2])
    return fib[:n]


def decrypt_fibonacci(cipher_text):
    fib = fibonacci(len(cipher_text))

    plain_text = ""

    for char, shift in zip(cipher_text, fib):
        plain_text += chr(ord(char) - shift)

    return plain_text


# Example encrypted text
encrypted = "Igopt"

decrypted = decrypt_fibonacci(encrypted)

print("Encrypted:", encrypted)
print("Decrypted:", decrypted)

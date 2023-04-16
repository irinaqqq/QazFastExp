import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e such that e and phi(n) are coprime
    # e = random.randrange(1, phi)
    e = 57
    while gcd(e, phi) != 1:
        # e = random.randrange(1, phi)
        e = 57
    print(e)
    # Calculate d such that d*e ≡ 1 (mod phi)
    d = pow(e, -1, phi)

    return ((n, e), (n, d))

def encrypt(pk, text):
    # Unpack the key into n and e
    n, e = pk
    # Convert each letter in the plaintext to numbers based on the character
    plaintext_bytes = text.encode('utf-8')
    # Encrypt the bytes using RSA
    ciphertext = [pow(b, e, n) for b in plaintext_bytes]
    # Return the array of bytes
    return ciphertext

def decrypt(pk, ciphertext):
    # Unpack the key into n and d
    n, d = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    ciphertext = [int(c) for c in ciphertext.split(',')]
    text = [chr(pow(c, d, n)) for c in ciphertext]
    # Return the array of bytes as a string
    return ''.join(text)


# p = 11
# q = 17
# public_key, private_key = generate_keypair(p, q)

# # Encrypt a message
# message = "some text more"
# ciphertext = encrypt(public_key, message)
# print("Ciphertext:", ciphertext)

# # Decrypt the message
# plaintext = decrypt(private_key, ciphertext)
# print("Plaintext:", plaintext)
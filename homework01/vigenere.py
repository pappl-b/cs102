import utils as u

def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keys = []
    keys_len = len(keyword)
    for letter in keyword.upper():
        keys.append(ord(letter) % 65)

    i = 0
    for letter in plaintext:
        letter_ord = ord(letter)
        if ord("A") <= letter_ord <= ord("Z"):
            ciphertext += chr(u.shifting(letter_ord, keys[i]))
        elif ord("a") <= letter_ord <= ord("z"):
            ciphertext += chr(u.shifting(letter_ord, keys[i], ord("a"), ord("z")))
        else:
            ciphertext += letter
        i += 1
        if i == keys_len:
            i = 0
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    keys = []
    keys_len = len(keyword)
    for letter in keyword.upper():
        keys.append(-(ord(letter) % 65))

    i = 0
    for letter in ciphertext:
        letter_ord = ord(letter)
        if ord("A") <= letter_ord <= ord("Z"):
            plaintext += chr(u.shifting(letter_ord, keys[i]))
        elif ord("a") <= letter_ord <= ord("z"):
            plaintext += chr(u.shifting(letter_ord, keys[i], ord("a"), ord("z")))
        else:
            plaintext += letter
        i += 1
        if i == keys_len:
            i = 0
    return plaintext

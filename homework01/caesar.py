import typing as tp

import utils as u


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for letter in plaintext:
        letter_ord = ord(letter)
        if ord("A") <= letter_ord <= ord("Z"):
            letter_ord = u.shifting(letter_ord, shift)
        elif ord("a") <= letter_ord <= ord("z"):
            letter_ord = u.shifting(letter_ord, shift, ord("a"), ord("z"))
        ciphertext += chr(letter_ord)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = encrypt_caesar(ciphertext, -shift)
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    shifts = [0] * 26
    for shift in range(26):
        shiftedtext = decrypt_caesar(ciphertext, shift).split()
        for word in shiftedtext:
            for key in dictionary:
                if key == word:
                    shifts[shift] += 1
                    break
    max_match = 0
    for i in range(26):
        if shifts[i] > max_match:
            max_match = shifts[i]
            best_shift = i
    return best_shift

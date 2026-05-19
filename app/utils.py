"""
utils.py — Generates unique short codes like "aB3xP7".

KEY CONCEPTS:
- Base62 encoding: uses 62 characters (a-z = 26, A-Z = 26, 0-9 = 10).
  With 6 characters you get 62^6 = ~56 billion possible combinations.
  That's enough for any real-world URL shortener.

- nanoid: a popular library (used in Node.js too) that generates
  cryptographically random IDs. Better than random.choice() in a loop
  because it uses the OS's secure random source (os.urandom).

- Collision: two different URLs accidentally getting the same short code.
  With 56 billion possibilities and 6-char codes, collisions are extremely
  rare, but we still check and retry in crud.py just to be safe.
  This is called a "retry on collision" pattern.
"""

from nanoid import generate

# Our alphabet: lowercase + uppercase letters + digits = 62 characters
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# 6 characters gives 62^6 ≈ 56 billion combinations
CODE_LENGTH = 6


def generate_short_code() -> str:
    """
    Generates a random 6-character string using Base62 alphabet.

    Examples of output: "aB3xP7", "mK92Lz", "Xr4tQ1"

    nanoid's generate() takes:
      - alphabet: the characters to pick from
      - size: how many characters long the result should be
    """
    return generate(ALPHABET, CODE_LENGTH)

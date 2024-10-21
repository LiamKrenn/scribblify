from hashlib import sha256


def hash(input):
    encoded = input.encode("utf-8")
    return sha256(encoded).hexdigest()

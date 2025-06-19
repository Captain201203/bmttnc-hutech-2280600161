import hashlib

def caculate_sha256_hash(data):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))  # Update with the input string as bytes
    return sha256_hash.hexdigest()

data_to_hash = input("Enter a string to hash: ")
hash_value = caculate_sha256_hash(data_to_hash)
print("SHA-256 hash of the string '{}' is: {}".format(data_to_hash, hash_value))
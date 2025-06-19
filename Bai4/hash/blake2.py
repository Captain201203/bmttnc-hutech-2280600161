import hashlib

def blake2_hash(message):
  
    blake2_hash = hashlib.blake2b(digest_size=32)  # Create a BLAKE2b hash object with a digest size of 32 bytes
    blake2_hash.update(message)
    return blake2_hash.digest()

def main():
    text = input("Enter a string to hash: ").encode('utf-8')
    hashed_text = blake2_hash(text)
    print("BLAKE2 hash of the string: ", text.decode('utf-8'))
    print("BLAKE2 hash value: ", hashed_text.hex())
    
if __name__ == "__main__":
    main()
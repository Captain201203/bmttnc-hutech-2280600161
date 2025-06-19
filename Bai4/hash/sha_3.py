from Crypto.Hash import SHA3_256

def sha3(message):
    sha3_hash = SHA3_256.new()
    sha3_hash.update(message)
    return sha3_hash.hexdigest()

def main():
    text = input("Enter a string to hash: ").encode('utf-8')
    hashed_text = sha3(text)
    
    print("Chuoi van ban da nhap: ", text.decode('utf-8'))
    print("SHA3-256 hash cua chuoi: ", hashed_text)
    
if __name__ == "__main__":
    main()
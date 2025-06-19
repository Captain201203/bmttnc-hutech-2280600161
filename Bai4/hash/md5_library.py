import hashlib

def caculate_md5(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))  # Update with the file path as bytes
    return md5_hash.hexdigest()

input_string = input("Enter a string to hash: ")
md5_hash = caculate_md5(input_string)
print("MD5 hash of the string '{}' is: {}".format(input_string, md5_hash))
import hashlib

flag = "my_flag_string_here"

# Convert the flag to bytes and hash with SHA-256
flag_bytes = flag.encode('utf-8')
hash_obj = hashlib.sha256(flag_bytes)
hash_str = hash_obj.hexdigest()

# Print the resulting hash
print("SHA-256 hash of flag: " + hash_str)
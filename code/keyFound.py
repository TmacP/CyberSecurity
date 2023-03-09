import zipfile

flag = "my_flag_string_here"
input_zip_file = "path/to/my_file.zip"

# Calculate the SHA-256 hash of the flag
flag_bytes = flag.encode('utf-8')
hash_obj = hashlib.sha256(flag_bytes)
hash_str = hash_obj.hexdigest()

# Check if the hash matches the expected value
if hash_str == "expected_hash_value":
    # Open the input ZIP file
    with zipfile.ZipFile(input_zip_file, 'r') as zip_ref:
        # Extract all files to a new directory
        zip_ref.extractall("path/to/my_output_directory")

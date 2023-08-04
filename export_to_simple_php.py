#================================================================
#Config

bakePath = "bake/"
resPath = "res/"
docsPath = "docs/"
adminPath = '.admin/' 

#================================================================
#libs

import os
import subprocess
import hashlib

#================================================================
#Functions

def delete_folder_contents(folder_path):
    #by chatGPT
    try:
        # Iterate over the folder contents
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                # If it's a file, delete it
                os.remove(file_path)
            elif os.path.isdir(file_path):
                # If it's a subdirectory, delete its contents recursively
                delete_folder_contents(file_path)
                # Delete the empty subdirectory
                os.rmdir(file_path)
    except OSError as e:
        print(f"Error deleting contents of {folder_path}: {e}")

def write_to_file_direct(file_path, data):
    try:
        with open(file_path, 'w+') as file:
            file.write(data)
            file.close()
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

def copy_folder(src_folder, dest_folder):
    try:
        # Create the destination folder if it doesn't exist
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        for root, _, files in os.walk(src_folder):
            relative_path = os.path.relpath(root, src_folder)
            dest_dir = os.path.join(dest_folder, relative_path)

            # Create the corresponding destination subdirectory if it doesn't exist
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            for file_name in files:
                src_file = os.path.join(root, file_name)
                dest_file = os.path.join(dest_dir, file_name)

                # Copy the file from the source to the destination directory
                copy_file_with_os(src_file, dest_file)
    except OSError as e:
        print(f"Error: {e}")

def copy_file_with_os(source_path, destination_path):
    try:
        with open(source_path, 'rb') as source_file:
            with open(destination_path, 'wb') as destination_file:
                # Read the content of the source file and write it to the destination file
                content = source_file.read()
                destination_file.write(content)
    except Exception as e:
        print(f"Error copying file: {e}")

def calculate_sha256_hash(input_string):
    # Convert the input string to bytes, as hashlib requires bytes-like objects
    input_bytes = input_string.encode('utf-8')

    # Calculate the SHA-256 hash
    sha256_hash = hashlib.sha256(input_bytes).hexdigest()

    return sha256_hash

#================================================================
#Correct config

adminPath = bakePath + adminPath

#================================================================
#Clear bake path

delete_folder_contents(bakePath)

#----------------------------------------------------------------
#Calc hashes

subprocess.run(["python", "calc_hashes.py"])

#----------------------------------------------------------------
#Copy source code

if os.path.exists(adminPath):
    delete_folder_contents(adminPath)
    os.rmdir(adminPath)
copy_folder('admin-simple_php', adminPath)
copy_file_with_os('bake.py', adminPath + 'bake.py')
copy_file_with_os('calc_hashes.py', adminPath + 'calc_hashes.py')
copy_file_with_os('hashes.dim', adminPath + 'hashes.dim')
copy_folder(docsPath, adminPath + 'docs')
copy_folder(resPath, adminPath + 'res')

#----------------------------------------------------------------
#Setup password

print("\n")
while True:
    password = input('Setup new Admin password: ')
    if input('Repeat password: ') == password:
        break
    else:
        print("Different passwords!\n")
password = calculate_sha256_hash(password)
write_to_file_direct(adminPath + 'passhash.key', password)
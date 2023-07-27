#================================================================
#libs

import os
import subprocess

#================================================================
#Functions

def write_to_file_direct(file_path, data):
    make_dir_by_filepath(file_path)
    #write to file
    try:
        with open(file_path, 'a+') as file:
            file.write(data)
            file.close()
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

def write_to_file(rel_path, data):
    write_to_file_direct(bakePath + rel_path, data)

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

#================================================================
#Consts

bakePath = "bake/"
resPath = "res/"
docsPath = "docs/"
adminPath = bakePath + 'admin/' 

#================================================================
#Bake

subprocess.run(["python", "bake.py"])

#----------------------------------------------------------------
#Calc hashes

subprocess.run(["python", "calc_hashes.py"])

#----------------------------------------------------------------
#Copy source code

copy_file_with_os('bake.py', adminPath + 'bake.py')
copy_file_with_os('calc_hashes.py', adminPath + 'calc_hashes.py')
copy_folder(docsPath, adminPath + 'docs')
copy_folder(resPath, adminPath + 'res')
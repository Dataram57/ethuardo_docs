#================================================================
#libs

import os
import markdown

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

def markdown_to_html(markdown_string):
    #by chatGPT
    try:
        # Convert the Markdown string to HTML
        html_string = markdown.markdown(markdown_string)
        return html_string
    except Exception as e:
        print(f"Error converting Markdown to HTML: {e}")
        return None

def read_file_into_string(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            return file_content
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def write_to_file_direct(file_path, data):
    #safely create directory
    file_dir = file_path[0: max(file_path.rfind('/'), file_path.rfind("\\"))]
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    #write to file
    try:
        with open(file_path, 'a+') as file:
            file.write(data)
            file.close()
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

def write_to_file(rel_path, data):
    write_to_file_direct(bakePath + rel_path, data)

def read_this_file():
    return read_file_into_string(true_target)

#================================================================
#Main

#clear console
if os.system('clear'):
    os.system('cls')

#Consts
bakePath = "bake"
setsPath = "sets"
docsPath = "docs"
#vars - informational
target = ""
target_dir = ""
target_title = ""
target_extentsion = ""
#vars - safe/security
true_target = ""
#vars
code = ""

#Clean folder content
delete_folder_contents(bakePath)

#scan each file
for root, dirs, files in os.walk(docsPath):
    for file in files:
        #basic info
        true_target = os.path.join(root, file)

        #make relative path
        target = true_target[len(docsPath):]
        target_dir = target[0: max(target.rfind('/'), target.rfind("\\")) + 1]
        target_extentsion = file[file.rfind('.') + 1:].lower()
        target_title = target[len(target_dir): len(target) - len(target_extentsion) - 1]
        #print('=============')
        #print("path:", target)
        #print("dir:", target_dir)
        #print("tit:", target_title)
        #print("ext:", target_extentsion)

        #MD
        if target_extentsion == "md":
            #correct path
            target = target_dir + target_title
            if target_title == "index":
                target += ".html"
            else:
                target += "/index.html"
            
            #read file
            code = read_this_file()
            
            #write
            write_to_file(target, markdown_to_html(code))
#end
print("Finished!")
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

def make_dir_by_filepath(file_path):
    #safely create directory
    file_path = file_path[0: max(file_path.rfind('/'), file_path.rfind("\\"))]
    if not os.path.exists(file_path):
        os.makedirs(file_path)

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

def read_this_file():
    return read_file_into_string(true_target)

def load_text_resource(rel_path):
    return read_file_into_string(resPath + rel_path)

def copy_file_with_os(source_path, destination_path):
    try:
        with open(source_path, 'rb') as source_file:
            with open(destination_path, 'wb') as destination_file:
                # Read the content of the source file and write it to the destination file
                content = source_file.read()
                destination_file.write(content)
    except Exception as e:
        print(f"Error copying file: {e}")

def copy_res_to_bake(rel_res_path, rel_bake_path):
    make_dir_by_filepath(bakePath + rel_bake_path)
    copy_file_with_os(resPath + rel_res_path, bakePath + rel_bake_path)

#================================================================
#Main

#clear console
if os.system('clear'):
    os.system('cls')

#Consts
bakePath = "bake/"
resPath = "res/"
docsPath = "docs/"
#vars - informational
target = ""
target_dir = ""
target_title = ""
target_extentsion = ""
#vars - informational special
target_last = ""
#vars - safe/security
true_target = ""
#vars
i = 0
code = ""

#----------------------------------------------------------------
#Clean folder content

delete_folder_contents(bakePath)

#----------------------------------------------------------------
#Copy consts

copy_res_to_bake('index.js','index.js')
copy_res_to_bake('index.css','index.css')

#----------------------------------------------------------------
#Read patterns

pat_page = [load_text_resource('page_1.html'), load_text_resource('page_2.html'), load_text_resource('page_3.html')]

#----------------------------------------------------------------
#generate tree
deep = ""
for root, dirs, files in os.walk(docsPath):
    for file in files:
        #basic info
        true_target = os.path.join(root, file)

        #make relative path
        target = true_target[len(docsPath):]
        target_dir = target[0: max(target.rfind('/'), target.rfind("\\")) + 1]
        target_extentsion = file[file.rfind('.') + 1:].lower()
        target_title = target[len(target_dir): len(target) - len(target_extentsion) - 1]
        if len(target_last) == 0:
            target_last = target_dir

        #MD (HOLY)
        if target_extentsion == "md":
            
            #check if entering new folder
            if target_last != target_dir:
                #calculate deep
                i = target_dir.count("/") + target_dir.count("\\")
                deep = ""
                while i > 0:
                    deep += "  "
                    i -= 1
                print(deep + target_dir[target_dir[0:-1].rfind("\\") + 1:-1] + ":")
            print(deep + "  -" + target_title)

        #update last dir
        target_last = target_dir

#----------------------------------------------------------------
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
            write_to_file(target, pat_page[0])
            #tree
            write_to_file(target, pat_page[1])
            write_to_file(target, markdown_to_html(code))
            write_to_file(target, pat_page[2])

#----------------------------------------------------------------
#end

print("Finished!")
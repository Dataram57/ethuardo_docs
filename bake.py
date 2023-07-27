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
                # check file skip
                file_path = file_path.replace("\\",'/')
                for skip in skip_folder_deletion:
                    if file_path[len(bakePath):] == skip:
                        file_path = ''
                        break
                if len(file_path) > 0:
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

def read_file_into_array(file_path):
    try:
        with open(file_path, 'r') as file:
            lines_array = file.readlines()
        return lines_array
    except Exception as e:
        return None

def get_name_by_path(path):
    return path[max(path.rfind('/'), path.rfind("\\")) + 1:]

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
    global true_target
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

def copy_res_folder_to_bake(rel_res_path, rel_bake_path):
    copy_folder(resPath + rel_res_path, bakePath + rel_bake_path)

def copy_docs_folder_to_bake(rel_res_path, rel_bake_path):
    copy_folder(docsPath + rel_res_path, bakePath + rel_bake_path)

def get_files_and_folders(directory):
    files_list = []
    folders_list = []

    # Get a list of all items (files and folders) within the directory
    items_list = os.listdir(directory)

    # Separate files and folders
    for item in items_list:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            files_list.append(item_path)
        elif os.path.isdir(item_path):
            folders_list.append(item_path)

    return files_list, folders_list

def cut_path_by_docs_path(path):
    return path[len(docsPath):]

def get_markdown_title(file_path):
    try:
        with open(docsPath + file_path, 'r') as file:
            return file.readline()[2:].strip()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def get_this_markdown_title():
    global true_target
    return get_markdown_title(cut_path_by_docs_path(true_target))

#================================================================
#Tree generation Mechanisms
tree_data = ""
tree_start = ""
tree_end = ""
tree_deep_level = 0
tree_print_space = '  '
tree_print_deep_space = ''

def print_tree_deep(message):
    global tree_deep_level, tree_print_deep_space
    print(tree_print_deep_space, message)

def generate_tree(file_path):
    #start building tree
    global tree_data, tree_start, tree_end, tree_deep_level, tree_print_deep_space, tree_print_space
    if tree_deep_level == 0:
        tree_data += tree_start
    tree_deep_level += 1
    tree_print_deep_space += tree_print_space

    #try to load .hierarchy
    hierarchy = read_file_into_array(file_path + '.hierarchy')
    if hierarchy is not None:
        for line in hierarchy:
            line = line.strip().strip()

            # Comment (#)
            if line[0] == '#':
                line = line[1:].strip()
                print_tree_deep('# ' + line)
                tree_data += render_comment(line)

            # Folder (/)
            elif line[0] == '/':
                line = line[1:].strip()
                print_tree_deep('V ' + line)
                line = file_path + line + '/'
                tree_data += render_folder_begin(cut_path_by_docs_path(line)) 
                #render another branch
                generate_tree(line)
                #end branch
                tree_data += render_folder_end() 
            
            # Etc... (...)
            elif line == '...':
                print_tree_deep('...Etc...')

            #Any other
            else:
                print_tree_deep('| ' + line)
                tree_data += render_option(cut_path_by_docs_path(file_path + line))
    
    #tree normally
    else:
        files, folders = get_files_and_folders(file_path)
        #files first
        for file in files:
            print_tree_deep('| ' + get_name_by_path(file))
            if get_name_by_path(file).lower() != 'index.md':
                tree_data += render_option(cut_path_by_docs_path(file))
        #folders
        for folder in folders:
            print_tree_deep('V ' + get_name_by_path(folder))
            folder += '/'
            tree_data += render_folder_begin(cut_path_by_docs_path(folder))
            #render another branch
            generate_tree(folder)
            #end branch
            tree_data += render_folder_end() 
    
    #end tree
    tree_deep_level -= 1
    tree_print_deep_space = tree_print_deep_space[:-len(tree_print_space)]
    if tree_deep_level == 0:
        tree_data += tree_end

#================================================================
#Main

#clear console
if os.system('clear'):
    os.system('cls')
print("Started...")

#Consts
bakePath = "bake/"
if not os.path.exists(bakePath):
    bakePath = '../'
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
title = ''

#----------------------------------------------------------------
#Clean folder content

skip_folder_deletion = ['admin']
delete_folder_contents(bakePath)

#----------------------------------------------------------------
#Copy consts

copy_res_to_bake('index.js','index.js')
copy_res_to_bake('index.css','index.css')
copy_res_to_bake('burger.svg','burger.svg')
copy_docs_folder_to_bake('img','img')

#----------------------------------------------------------------
#Read patterns and define its functions

pat_page = [load_text_resource('page_1.html'), load_text_resource('page_2.html'), load_text_resource('page_3.html'), load_text_resource('page_4.html')]
pat_folder = [load_text_resource('folder_1.html'), load_text_resource('folder_2.html'), load_text_resource('folder_3.html'), load_text_resource('folder_4.html')]
pat_option = [load_text_resource('option_1.html'), load_text_resource('option_2.html'), load_text_resource('option_3.html')]
pat_comment = [load_text_resource('comment_1.html'), load_text_resource('comment_2.html')]

tree_start = '<ul>'
tree_end = '</ul>'

def render_folder_begin(folder_path):
    return pat_folder[0] + get_markdown_title(folder_path + 'index.md') + pat_folder[1] + '/' + folder_path + pat_folder[2]

def render_folder_end():
    return pat_folder[3]

def render_option(file_path):
    return pat_option[0] + '/' + file_path[:-3] + '/' + pat_option[1] + get_markdown_title(file_path) + pat_option[2]

def render_comment(header):
    return pat_comment[0] + header + pat_comment[1]

#----------------------------------------------------------------
#Generate tree

generate_tree(docsPath)
#write_to_file("tree.html", tree_data)

#----------------------------------------------------------------
#Scan each file

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
            target = target.replace("\\",'/')

            #read file
            code = read_this_file()
            code = markdown_to_html(code)
            title = get_this_markdown_title()
            #write
            write_to_file(target, pat_page[0])
            write_to_file(target, '<title>' + title + '</title>')
            write_to_file(target, pat_page[1])
            write_to_file(target, tree_data)
            write_to_file(target, pat_page[2])
            write_to_file(target, code)
            write_to_file(target, pat_page[3])

#----------------------------------------------------------------
#end

print("Finished!")
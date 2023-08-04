#================================================================
#Libs

import os
import subprocess

#================================================================
#Main

subprocess.run(["python", "remote_push.py"])
#clear
if os.system('clear'):
    os.system('cls')
subprocess.run(["python", "remote_bake.py"])

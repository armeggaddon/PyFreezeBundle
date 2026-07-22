import os
from cx_Freeze import setup, Executable

def read_requirements(file_name):
    
    with open(file_name) as f:
        return [line.strip() for line in f]
    
project_path = os.path.dirname(os.path.realpath(__file__))  

file_list = []    
file_list.append(f"{project_path}/test")

includefiles = file_list
file_name = project_path+'/'+'requirements.txt'
i_packages = read_requirements(file_name)
e_packages = ['setuptools','pip','cx_Freeze']

application_name = 'PyFreezeBundle'
build_path = project_path +'/'+ application_name

# "build_exe": build_path,
#setup to create a EXE file
exe = [Executable("./main.py")]
options = {"build_exe": {'build_exe': build_path,'packages':i_packages,'excludes':e_packages,'include_files':includefiles}}
setup(
    name="PyFreezeBundle",                      
    version="1.0.0",                            
    description="PyFreeze bundle demo",               
    options = options,
    executables=exe,
)


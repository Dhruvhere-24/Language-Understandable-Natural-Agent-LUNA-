## Directory Traversal controller
import os 

def get_current_dir():
    return os.getcwd()

def folders_only():
    return [i for i in list(os.listdir(get_current_dir())) if os.path.isdir(i)]

def file_only():
    return [i for i in list(os.listdir(get_current_dir())) if os.path.isfile(i)]

def move_dir(name): 
    os.chdir(str(name))


print(folders_only())
print(file_only())

move_dir(folders_only()[0])
print(get_current_dir())

print(folders_only())
print(file_only())

### Now expand this try it 
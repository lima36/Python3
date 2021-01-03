import os
import re
from os.path import isfile, join

def listdir(dirName, filelist=[]):
    print(dirName)
    print(os.listdir(dirName))

    # files = [f for f in os.listdir(dirName) if re.match(r'.log', f)]
    files = os.listdir(dirName)
    for file in files:
        if file.endswith(".log"):
            print("listdir: ", file)
            filelist.append(join(dirName, file))

    return filelist


# List all files in the directory
# Return all list
def listAllFile(dirName, ext):
    fileList = list()
    for file in os.listdir(dirName):
        if file.endswith(ext):
            fileList.append([os.path.join(dirName, file)])
            print(os.path.join(dirName, file))

    # name sorting
    # fileList.sort(key=lambda f: int(filter(str.isdigit, f) or -1))
    return fileList
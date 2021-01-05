import os
import re
from os.path import isfile, join


def listdir(dirName, filelist=[]):
    print(dirName)
    print(os.listdir(dirName))

    # files = [f for f in os.listdir(dirName) if re.match(r'.log', f)]
    files = sorted(os.listdir(dirName))
    filelist = []
    for file in files:
        if file.endswith(".log"):
            print("listdir: ", file)
            filelist.append(join(dirName, file))

    return filelist


# List all files in the directory
# Return all list
def listAllFile(dirName, ext):
    fileList = []
    for file in os.listdir(dirName):
        if file.endswith(ext):
            fileList.append([os.path.join(dirName, file)])
            print(os.path.join(dirName, file))

    # name sorting
    # fileList.sort(key=lambda f: int(filter(str.isdigit, f) or -1))
    return fileList


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)
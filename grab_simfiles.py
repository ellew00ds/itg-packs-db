import os

from pprint import pprint

###
# expects rootdir to contain directories
# from extracted sm packs at top level
###


def grab_simfiles(rootdir, path_array=[], simfile_array=[]):
    for subdir, dirs, files in os.walk(rootdir):
        path = subdir.split('/')
        print("\n****** - Next Song Dir -", '*' * 50)
        if len(path) > 2:
            path_array.append(path)
            for path in path_array:
                #print(f"pack_name: {path[1]} -- song_name: {path[2]}")
                pass

        for file in files:
            #print("os.path.join(subdir, file):", os.path.join(subdir, file))
            if file.lower().endswith(('.scc', '.sm')):
                print(f"KICKASS BRO: '{file}' is a simfile")
                simfile_array.append(os.path.join(subdir, file))
                #print("simfile_array:", simfile_array)
            else:
                print(f"IGNORED: '{file}' is not a simfile")
        print('*' * 75, '\n')
    return simfile_array

if __name__ == "__main__":
    rootdir = 'packs'
    simfile_array = grab_simfiles(rootdir)
    print("simfile_array in main:")
    for simfile in simfile_array:
        print(simfile)

import os
import sys
import platform

def inplace_change(filename, old_string, new_string):
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if old_string not in s:
            print('"{old_string}" not found in {filename}.'.format(**locals()))
            return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
        s = s.replace(old_string, new_string)
        f.write(s)

def getLibOTe(install, prefix, par,libOTe, boost, relic):

    cwd = os.getcwd()

    if os.path.isdir("libOTe") == False:
        os.system("git clone --recursive https://github.com/osu-crypto/libOTe.git")

    os.chdir(cwd + "/libOTe")
    os.system("git checkout 2363505431f744539027a873c2536b9ae3630ff7 --quiet ")
    os.system("git submodule update ")

    #---------------- Edit CMakeLists.txt in cryptoTools, since it ignores the flag for this commit
    cmake_lists = 'cryptoTools/CMakeLists.txt'
    to_replace = 'option(ENABLE_CIRCUITS  "compile the circuit module" OFF)'
    new_expression = 'option(ENABLE_CIRCUITS  "compile the circuit module" ON)'
    inplace_change(cmake_lists, to_replace, new_expression)
    #-------------- Finish editing CMakeLists.txt

    osStr = (platform.system())

    debug = ""
    if "--debug" in sys.argv:
        debug = " --debug "

    sudo = ""
    if(osStr == "Windows"):
        if not install:
            prefix = cwd + "/win"
            if len(debug):
                prefix += "-debug"

    else:
        if not install:
            prefix = cwd + "/unix"
        if install and "--sudo" in sys.argv:
            sudo = "--sudo "



    installCmd = ""
    if len(prefix) > 0:
        installCmd = "--install=" + prefix
    elif install:
        installCmd = "--install"

    cmakePrefix = ""
    if len(prefix) > 0:
        cmakePrefix = "-DCMAKE_PREFIX_PATH=" + prefix

    cmd =  "python3 build.py " + sudo + " --par=" + str(par) + " " + installCmd + " " + debug
    boostCmd = cmd + " --setup --boost "
    relicCmd = cmd + " --setup --relic "
    libOTeCmd = cmd + " -DENABLE_CIRCUITS=ON " + cmakePrefix;


    print("\n\n=========== getLibOTe.py ================")
    if boost:
        print(boostCmd)
    if relic:
        print(relicCmd)
    if libOTe:
        print(libOTeCmd)
    print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\n\n")

    if boost:
        os.system(boostCmd)
    if relic:
        os.system(relicCmd)
    if libOTe:
        os.system(libOTeCmd)

    os.chdir(cwd)

if __name__ == "__main__":
    getLibOTe(False, "", 1, True, True, True)

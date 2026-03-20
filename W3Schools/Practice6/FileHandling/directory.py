import os

testfolder = "WORKSPACE"
value = os.getenv(testfolder)

os.chdir(value)
print ("Current directory:" , os.getcwd())

os.mkdir("mydir")

os.chdir("mydir")

print ("Updated directory:" , os.getcwd())
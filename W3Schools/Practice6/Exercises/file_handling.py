import os
import shutil

# 1.
with open("example.txt", "w") as f:
    f.write("Hello, World!\nSome data will be here.")

# 2.
with open("example.txt", "r") as f:
    print("File content:", f.read())

# 3. 
with open("example.txt", "a") as f:
    f.write("\nUpdated information.")

with open("example.txt", "r") as f:
    print(f.read())
# 4.
shutil.copy("example.txt", "example_backup.txt")
print("Backup created")

# 5.
if os.path.exists("example_backup.txt"):
    os.remove("example_backup.txt")
    print("File deleted")
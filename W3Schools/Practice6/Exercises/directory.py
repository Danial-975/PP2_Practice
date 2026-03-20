import os
import shutil

# 1. 
os.makedirs("parent/child/grandchild", exist_ok=True)

# 2. 
print("List of files and directories:", os.listdir("."))

# 3. 
txt_files = [f for f in os.listdir(".") if f.endswith(".txt")]
print("Text files:", txt_files)

# 4.
with open("move_me.txt", "w") as f: f.write("test")
shutil.move("move_me.txt", "parent/child/move_me.txt")
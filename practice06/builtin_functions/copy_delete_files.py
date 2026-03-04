#1
import os
os.remove("demofile.txt")
#2
import os
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist")ы
#3
import os
os.rmdir("myfolder")

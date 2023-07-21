import os
import sys

root_path=(os.path.split(os.path.split(os.path.split(sys.path[0])[0])[0])[0]) # Obtaining root path of Project
sys.path.insert(0, root_path + '\config')
print(root_path + '\config')

from test import Asta

Asta()

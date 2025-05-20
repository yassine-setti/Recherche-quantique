import os
for file in os.listdir(r"C:\Users\yassi\Desktop\2A\Recherche\Scripts"):
        if file.endswith(".png") or file.endswith(".jpg"):
            os.remove(os.path.join(r"C:\Users\yassi\Desktop\2A\Recherche\Scripts", file))
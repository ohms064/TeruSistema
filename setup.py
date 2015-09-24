import os
os.system("git pull")
print("Ultima modificacion:\n")
os.system("git log -1 --pretty=%B")
input("\n\nPresione una tecla para continuar...")

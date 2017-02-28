import os
out = os.system("git pull")
print("Ultima modificacion:\n")
os.system("git log -1 --pretty=%B")
print(out)
input("\n\nPresione enter para continuar...")

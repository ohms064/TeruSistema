import os
os.system("git pull")
print("Última modificación:\n")
os.system("git log -1 --pretty=%B")
input("\n\nPresione una tecla para continuar...")
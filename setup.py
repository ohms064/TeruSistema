import os
os.system("git pull")
print("�ltima modificaci�n:\n")
os.system("git log -1 --pretty=%B")
input("\n\nPresione una tecla para continuar...")
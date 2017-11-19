import re

try:
   f = open("spectre.conf",'r+')
except:
   banner="Unable to Open file spectre.conf"

x=f.read()
y = re.split("\n",x)
z=[]
for i in range(len(y)):
     if(y[i])!='':
             z.append(y[i])

print z
f.close()




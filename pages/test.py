from db import Setup
import pandas as pd

lista = Setup().db.child("Logs/Máquina 1/LogVelocidade").get()

lista1 = []
lista2 = []

for i in lista.each():
    a = i.key()
    lista1.append(a)

df1 = pd.DataFrame(lista1,columns=['Timestamp'])

for i in lista.each():
    b = i.val()
    lista2.append(b)

df2 = pd.DataFrame(lista2)

df3 = pd.concat([df1,df2['Velocidade']],axis=1)

print(df3)

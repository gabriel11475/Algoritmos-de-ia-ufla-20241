import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import numpy as np
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_iris

# fetch dataset 
iris = load_iris() 
  
# data (as pandas dataframes) 
iristodasasmedidas= iris.data
iristodasclassificacoes = iris.target
iristodasclassificacoes = iristodasclassificacoes.ravel()
irisaprendizado = []
irisaprendizadotarget = []

iristeste =[]
iristestetarget = []

for i in range (0, len(iristodasasmedidas)):
    if(i%3==0):
        iristeste.append(iristodasasmedidas[i])
        iristestetarget.append(iristodasclassificacoes[i])
    else:
        irisaprendizado.append(iristodasasmedidas[i])
        irisaprendizadotarget.append(iristodasclassificacoes[i])
print(str(len(iristeste))+ " amostras para testar o Iris dataset:")
knn = KNeighborsClassifier(n_neighbors=7)
knn.fit(irisaprendizado, irisaprendizadotarget)
irispredknn = knn.predict(iristeste)

#print(irispred)
acuraciasirisknn7= accuracy_score(iristestetarget, irispredknn)
precisaosirisknn7 = precision_score(iristestetarget, irispredknn, average="macro")
revocacaosirisknn7 = recall_score(iristestetarget, irispredknn, average="macro")
matrizconfusaoirisknn7 = confusion_matrix(iristestetarget, irispredknn)

scaler = StandardScaler()
irisaprendizadoescalado= scaler.fit_transform(irisaprendizado)
iristesteescalado = scaler.transform(iristeste)

# Criar o classificador MLP
mlp = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)

# Treinar o classificador
mlp.fit(irisaprendizadoescalado, irisaprendizadotarget)

# Fazer previsões no conjunto de teste
irispredmlp = mlp.predict(iristesteescalado)
acuraciairismlp= accuracy_score(iristestetarget, irispredmlp)
precisaosirismlp = precision_score(iristestetarget, irispredmlp, average="macro")
revocacaosirismlp = recall_score(iristestetarget, irispredmlp, average="macro")
matrizconfusaoirismlp = confusion_matrix(iristestetarget, irispredmlp)
print("Para Iris dataset:")
print("matriz de confusao knn \t matriz de confusao mlp")
for i in range(len(matrizconfusaoirisknn7)):
    print(str(matrizconfusaoirisknn7[i][0])+" "+str(matrizconfusaoirisknn7[i][1])+" "+str(matrizconfusaoirisknn7[i][2])+" "+ "\t\t\t\t"+ str(matrizconfusaoirismlp[i][0])+" "+ str(matrizconfusaoirismlp[i][1])+" "+str(matrizconfusaoirismlp[i][2]))

print("KNN\tAcuracia: "+str(acuraciasirisknn7) +" precisao: "+ str(precisaosirisknn7)+"\t revocacao: "+str(revocacaosirisknn7))
print("MLP\tAcuracia: "+str(acuraciairismlp) +" precisao: "+ str(precisaosirismlp)+"\t revocacao: "+str(revocacaosirismlp))

from sklearn.datasets import load_wine

wine = load_wine()
winetodasasmedidas = wine.data
winetodasclassificacoes = wine.target

wineaprendizado = []
wineaprendizadotarget = []

wineteste =[]
winetestetarget = []

for i in range (0, len(winetodasasmedidas)):
    if(i%3==0):
        wineteste.append(winetodasasmedidas[i])
        winetestetarget.append(winetodasclassificacoes[i])
    else:
        wineaprendizado.append(winetodasasmedidas[i])
        wineaprendizadotarget.append(winetodasclassificacoes[i])
print(str(len(wineteste))+ " amostrar para testar Wine dataset:")
knn = KNeighborsClassifier(n_neighbors=7)
knn.fit(wineaprendizado, wineaprendizadotarget)
winepredknn = knn.predict(wineteste)

#print(irispred)
acuraciaswineknn7= accuracy_score(winetestetarget, winepredknn)
precisaoswineknn7 = precision_score(winetestetarget, winepredknn, average="macro")
revocacaoswineknn7 = recall_score(winetestetarget, winepredknn, average="macro")
matrizconfusaowineknn7 = confusion_matrix(winetestetarget, winepredknn)

scaler = StandardScaler()
wineaprendizadoescalado= scaler.fit_transform(wineaprendizado)
winetesteescalado = scaler.transform(wineteste)

# Criar o classificador MLP
mlp = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)

# Treinar o classificador
mlp.fit(wineaprendizadoescalado, wineaprendizadotarget)

# Fazer previsões no conjunto de teste
winepredmlp = mlp.predict(winetesteescalado)
acuraciawinemlp= accuracy_score(winetestetarget, winepredmlp)
precisaoswinemlp = precision_score(winetestetarget, winepredmlp, average="macro")
revocacaoswinemlp = recall_score(winetestetarget, winepredmlp, average="macro")
matrizconfusaowinemlp = confusion_matrix(winetestetarget, winepredmlp)
print("Para Wine dataset:")
print("matriz de confusao knn \t matriz de confusao mlp")
for i in range(len(matrizconfusaowineknn7)):
    print(str(matrizconfusaowineknn7[i][0])+" "+str(matrizconfusaowineknn7[i][1])+" "+str(matrizconfusaowineknn7[i][2])+" "+ "\t\t\t\t"+ str(matrizconfusaowinemlp[i][0])+" "+ str(matrizconfusaowinemlp[i][1])+" "+str(matrizconfusaowinemlp[i][2]))

print("KNN\tAcuracia: "+str(acuraciaswineknn7) +" precisao: "+ str(precisaoswineknn7)+"\t revocacao: "+str(revocacaosirisknn7))
print("MLP\tAcuracia: "+str(acuraciawinemlp) +" precisao: "+ str(precisaoswinemlp)+"\t revocacao: "+str(revocacaoswinemlp))
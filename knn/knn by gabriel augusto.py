import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from ucimlrepo import fetch_ucirepo 
import numpy as np
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score

# fetch dataset 
iris = fetch_ucirepo(id=53) 
  
# data (as pandas dataframes) 
todasasmedidas= iris.data.features 
todasclassificacoes = iris.data.targets 

#separando os dados, de 150 classificacoes, 100 serao usadas para comparar as 50 restantes, pegando o 5o elemento de cada grupo para
#gerar os casos de teste

medidasbase= []
classificacaobase = []
medidasteste = []
classificacaoteste= []

#SPLIT, separando os dados, o 5o elemento do grupo vai virar um dado de teste
#salva os dados no formato (indice original, valores)
for i in range (0,150):
    if(i%5==0):
        medidasteste.append((i, todasasmedidas.iloc[i]))
    else:
        medidasbase.append((i, todasasmedidas.iloc[i]))
        classificacaobase.append((i, todasclassificacoes.iloc[i]))

#calcula distancia euclidiana, a e b devem ter a mesma dimensão na segunda tupla, que está no formato (indice, elemento[dimensoes])
def distanciaEuclidiana(a, b):
    soma = 0
    for i in range(0, len(a[1])):
        soma += (a[1][i] - b[1][i])**2
    #print(str(soma))
    return soma**(0.5)

#KNN calcula a distancia de todos os elementos de database com element, escolhe os ksize vizinhos mais proximos e o classifica
#de acordo com os a classificação dos vizinhos
def KNN( Ksize, database, element):
    distancias = []
    for i in range (0, len(database)):
        distancias.append( (i, distanciaEuclidiana(database[i], element) ) )
    distancias.sort(key= lambda x: x[1])
    
    contTypeA =0
    contTypeB =0
    contTypeC =0
    maior=0
    tipodomaior = ''
    empate = True
    for k in range(0,Ksize):
        #print(str(k)+ "o elemento comparado é de indice nos na classificacaobase "+ str(distancias[k][0]) + " e possui distancia "+ str(distancias[k][1]) )
        #print("E possui tais caracteristicas no classificacao base: "  + str(classificacaobase[distancias[k][0]][1]))
        #print("E no todasclassficacoes está como "+ todasclassificacoes.iloc[medidasbase[distancias[k][0]][0]])
        if(classificacaobase[distancias[k][0]][1]=="Iris-setosa").any():
            contTypeA+=1
            if(contTypeA > maior):
                empate = False
                maior = contTypeA
                tipodomaior = 'a'
            elif(contTypeA == maior):
                empate = True
        elif(classificacaobase[distancias[k][0]][1]== "Iris-versicolor").any():
            contTypeB+=1
            if(contTypeB > maior):
                empate = False
                maior = contTypeB
                tipodomaior = 'b'
            elif(contTypeB == maior):
                empate = True
        elif(classificacaobase[distancias[k][0]][1]=="Iris-virginica").any():
            contTypeC+=1
            if(contTypeC > maior):
                empate=False
                maior= contTypeB
                tipodomaior = 'c'
            elif(contTypeC == maior):
                empate = True
    print("O elemento comparado no todasclassificacoes está como: "+ str(todasclassificacoes.iloc[element[0]]))
    if(empate):
        print("empate")
        maisperto = distancias[0][0]
        return classificacaobase[maisperto][1]
    else:
        match tipodomaior:
            case 'a':
                return "Iris-setosa"
            case 'b':
                return "Iris-versicolor"
            case 'c': 
                return "Iris-virginica"
            case _:
                return "nao deu certo"

def acc_prec_rev( tamanho, matriz):
    truepositiive = 0
    truenegative = 0
    falsenegative =0 
    falsepositive = 0 
#gerador de matriz de confusao, para cada classificacao possivel é criado uma linha e coluna, inicialmente m[x][y]=0
#depois percorre dois vetores comparando os valores e incrementando suas respectivas 
def geradordematrizdeconfusao (numerodeclassificacoes, valoresreais, valoresprevistos):
    matriz = [[None] * numerodeclassificacoes for _ in range(numerodeclassificacoes)]
    for i in range (0, numerodeclassificacoes):
        for j in range (0, numerodeclassificacoes):
            matriz[i][j]=0
    for i in range(0, len(valoresreais)):
        valorreal = valoresreais[i]
        valorprevisto = valoresprevistos[i]
        linha = -1
        coluna = -1
        if(type(valorreal) != int):
            if(valorreal.iloc[0] == "Iris-setosa"):
                linha =0
            elif(valorreal.iloc[0]=="Iris-versicolor"):
                linha=1
            elif(valorreal.iloc[0] == "Iris-virginica"):
                linha=2
        else:
            linha = valorreal
        if(valorprevisto == "Iris-setosa"):
            coluna =0
        elif(valorprevisto=="Iris-versicolor"):
            coluna=1
        elif(valorprevisto == "Iris-virginica"):
            coluna=2
        else:
            coluna = valorprevisto
        matriz[linha][coluna]+=1
    return matriz

def classificacaoEmNumero( valor):
    classificacao = -1
    if(valor == "Iris-setosa").any():
        classificacao= 0
    elif(valor=="Iris-versicolor").any():
        classificacao = 1
    elif(valor== "Iris-virginica").any():
        classificacao = 2

    return classificacao

k = 1
while(k<9):
    for i in range(0, len(medidasteste)):
        classificacaoteste.append((k, medidasteste[i][0], KNN(k, medidasbase, medidasteste[i])))
    k+=2

taxadeacertok1 =0
taxadeacertok3 = 0
taxadeacertok5 =0
taxadeacertok7=0
for i in classificacaoteste:
    if( i[2] == todasclassificacoes.iloc[i[1]]).any():
        print(str(i[0]) +" acertou a classficacao de " +str(i[1]) )
        if(i[0]==1):
            taxadeacertok1+=1
        elif(i[0]==3):
            taxadeacertok3+=1
        elif(i[0]==5):
            taxadeacertok5+=1
        elif(i[0]==7):
            taxadeacertok7+=1
    else:
        print(str(i[0]) +" errou a classficacao de " +str(i[1]) )

valoresreais = [None]*30
valoresprevistos = [None]*30

for i in range (0,30):
    valoresreais[i] = todasclassificacoes.iloc[classificacaoteste[i][1]]
    valoresprevistos[i] = classificacaoteste[i][2]
matrizconfusaok1 = geradordematrizdeconfusao(3, valoresreais, valoresprevistos)
print("Taxa de acerto da minha implementação para o knn com k = 1 foi de: " + str((taxadeacertok1/30)*100) +"%")
print("matriz de confusao para k=1")
for i in range (0,len(matrizconfusaok1[0])):
    print(str(matrizconfusaok1[i][0])+ "\t" +str(matrizconfusaok1[i][1])+ "\t"+ str(matrizconfusaok1[i][2]))
acuraciak1 = accuracy_score(valoresreais, valoresprevistos)
precisaok1 = precision_score(valoresreais, valoresprevistos, average="macro")
revocacaok1 = recall_score(valoresreais, valoresprevistos, average="macro")

print("Taxa de acerto da minha implementação para o knn com k = 3 foi de: " + str((taxadeacertok3/30)*100)+"%")
for i in range (0,30):
    pos = i+30
    valoresreais[i] = todasclassificacoes.iloc[classificacaoteste[pos][1]]
    valoresprevistos[i] = classificacaoteste[pos][2]
matrizconfusaok3 = geradordematrizdeconfusao(3, valoresreais, valoresprevistos)
print("matriz de confusao para k=3")
for i in range (0,len(matrizconfusaok3[0])):
    print(str(matrizconfusaok3[i][0])+ "\t" +str(matrizconfusaok3[i][1])+ "\t"+ str(matrizconfusaok3[i][2]))
acuraciak3 = accuracy_score(valoresreais, valoresprevistos)
precisaok3 = precision_score(valoresreais, valoresprevistos, average="macro")
revocacaok3 = recall_score(valoresreais, valoresprevistos, average="macro")

print("Taxa de acerto da minha implementação para o knn com k = 5 foi de: " + str((taxadeacertok5/30)*100)+"%")
for i in range (0,30):
    valoresreais[i] = todasclassificacoes.iloc[classificacaoteste[i+60][1]]
    valoresprevistos[i] = classificacaoteste[i+60][2]
matrizconfusaok5 = geradordematrizdeconfusao(3, valoresreais, valoresprevistos)
print("matriz de confusao para k=5")
for i in range (0,len(matrizconfusaok5[0])):
    print(str(matrizconfusaok5[i][0])+ "\t" +str(matrizconfusaok5[i][1])+ "\t"+ str(matrizconfusaok5[i][2]))
acuraciak5 = accuracy_score(valoresreais, valoresprevistos)
precisaok5 = precision_score(valoresreais, valoresprevistos, average="macro")
revocacaok5 = recall_score(valoresreais, valoresprevistos, average="macro")

print("Taxa de acerto da minha implementação para o knn com k = 7 foi de: " + str((taxadeacertok7/30)*100)+"%")
for i in range (0,30):
    valoresreais[i] = todasclassificacoes.iloc[classificacaoteste[i+90][1]]
    valoresprevistos[i] = classificacaoteste[i+90][2]
matrizconfusaok7 = geradordematrizdeconfusao(3, valoresreais, valoresprevistos)
print("matriz de confusao para k=7")
for i in range (0,len(matrizconfusaok7[0])):
    print(str(matrizconfusaok7[i][0])+ "\t" +str(matrizconfusaok7[i][1])+ "\t"+ str(matrizconfusaok7[i][2]))
acuraciak7 = accuracy_score(valoresreais, valoresprevistos)
precisaok7 = precision_score(valoresreais, valoresprevistos, average="macro")
revocacaok7 = recall_score(valoresreais, valoresprevistos, average="macro")

from sklearn.neighbors import KNeighborsClassifier

classificacaotestesk = []
k=1
i = 0
vetormedidasbase= []
vetorclassificacaobase = []
for i in range(0, len(medidasbase)):
    vetormedidasbase.append([medidasbase[i][1][0], medidasbase[i][1][1], medidasbase[i][1][2], medidasbase[i][1][0]])
    valor=classificacaobase[i][1]
    if(valor.iloc[0] == "Iris-setosa"):
        vetorclassificacaobase.append(0)
    elif(valor.iloc[0]=="Iris-versicolor"):
        vetorclassificacaobase.append(1)
    elif(valor.iloc[0] == "Iris-virginica"):
        vetorclassificacaobase.append(2)

k = 1
classificacaotestesk = []

#parte de testar o knn do sklearn, para cadas k(1,3,5,7) treina o knn, faz um vetor com as medidas para serem testadas
#e faz a previsão para esses testes, e guarda o resultado em outro vetor
while k <= 7:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(vetormedidasbase, vetorclassificacaobase)
    array = []
    for i in range(0, len(medidasteste)):
        array.append([medidasteste[i][1][0], medidasteste[i][1][1], medidasteste[i][1][2], medidasteste[i][1][0]])
    array_pred = knn.predict(array)
    for i in range(len(array_pred)):
        classificacaotestesk.append((k, medidasteste[i][0], array_pred[i]))
    k += 2

#print(classificacaotestesk)
for i in range (0,30):
    valorreal = todasclassificacoes.iloc[classificacaoteste[i][1]]
    valoresreais[i] = classificacaoEmNumero(valorreal)
    valoresprevistos[i] = classificacaotestesk[i][2]
matrizconfusaoskk1 = geradordematrizdeconfusao(3, valoresreais, valoresprevistos)
taxadeacertoskk1=0
for i in range(0, len(matrizconfusaoskk1)):
    taxadeacertoskk1+=matrizconfusaoskk1[i][i]
print("Taxa de acerto da implementação do sklearn para o knn com k = 1 foi de: " + str((taxadeacertoskk1/30)*100))
print("matriz de confusao para k=1")
for i in range (0,len(matrizconfusaoskk1[0])):
    print(str(matrizconfusaoskk1[i][0])+ "\t" +str(matrizconfusaoskk1[i][1])+ "\t"+ str(matrizconfusaoskk1[i][2]))
acuraciaskk1 = accuracy_score(valoresreais, valoresprevistos)
precisaoskk1 = precision_score(valoresreais, valoresprevistos, average="macro")
revocacaoskk1 = recall_score(valoresreais, valoresprevistos, average="macro")
for i in range (0,30):
    valorreal = todasclassificacoes.iloc[classificacaoteste[i+30][1]]
    valoresreais[i] = classificacaoEmNumero(valorreal)
    valoresprevistos[i] = classificacaotestesk[i+30][2]
matrizconfusaoskk3 = geradordematrizdeconfusao(3, valoresreais, valoresprevistos)
taxadeacertoskk3=0
for i in range(0, len(matrizconfusaoskk1)):
    taxadeacertoskk3+=matrizconfusaoskk3[i][i]
print("Taxa de acerto da implementação do sklearn para o knn com k = 3 foi de: " + str((taxadeacertoskk3/30)*100))
print("matriz de confusao para k=3")
for i in range (0,len(matrizconfusaoskk3[0])):
    print(str(matrizconfusaoskk3[i][0])+ "\t" +str(matrizconfusaoskk3[i][1])+ "\t"+ str(matrizconfusaoskk3[i][2]))
acuraciaskk3 = accuracy_score(valoresreais, valoresprevistos)
precisaoskk3 = precision_score(valoresreais, valoresprevistos, average="macro")
revocacaoskk3 = recall_score(valoresreais, valoresprevistos, average="macro")
for i in range (0,30):
    valorreal = todasclassificacoes.iloc[classificacaoteste[i+60][1]]
    valoresreais[i] = classificacaoEmNumero(valorreal)
    valoresprevistos[i] = classificacaotestesk[i+60][2]
matrizconfusaoskk5 = geradordematrizdeconfusao(3, valoresreais, valoresprevistos)
taxadeacertoskk5=0
for i in range(0, len(matrizconfusaoskk1)):
    taxadeacertoskk5+=matrizconfusaoskk5[i][i]
print("Taxa de acerto da implementação do sklearn para o knn com k = 5 foi de: " + str((taxadeacertoskk5/30)*100))
print("matriz de confusao para k=5")
for i in range (0,len(matrizconfusaoskk5[0])):
    print(str(matrizconfusaoskk5[i][0])+ "\t" +str(matrizconfusaoskk5[i][1])+ "\t"+ str(matrizconfusaoskk5[i][2]))
acuraciaskk5 = accuracy_score(valoresreais, valoresprevistos)
precisaoskk5 = precision_score(valoresreais, valoresprevistos, average="macro")
revocacaoskk5 = recall_score(valoresreais, valoresprevistos, average="macro")

for i in range (0,30):
    valorreal = todasclassificacoes.iloc[classificacaoteste[i+90][1]]
    valoresreais[i] = classificacaoEmNumero(valorreal)
    valoresprevistos[i] = classificacaotestesk[i+90][2]
matrizconfusaoskk7 = geradordematrizdeconfusao(3, valoresreais, valoresprevistos)
taxadeacertoskk7=0
for i in range(0, len(matrizconfusaoskk1)):
    taxadeacertoskk7+=matrizconfusaoskk7[i][i]
print("Taxa de acerto da implementação do sklearn para o knn com k = 7 foi de: " + str((taxadeacertoskk7/30)*100))
print("matriz de confusao para k=7")
for i in range (0,len(matrizconfusaoskk7[0])):
    print(str(matrizconfusaoskk7[i][0])+ "\t" +str(matrizconfusaoskk7[i][1])+ "\t"+ str(matrizconfusaoskk7[i][2]))
acuraciaskk7 = accuracy_score(valoresreais, valoresprevistos)
precisaoskk7 = precision_score(valoresreais, valoresprevistos, average="macro")
revocacaoskk7 = recall_score(valoresreais, valoresprevistos, average="macro")

print("Comparando desempenho dos dois classificadores")
print("A acuracia para k=1 da minha implementação foi de: " + str(acuraciak1) + " do sklearn foi: " + str(acuraciaskk1))
print("A precisao para k=1 da minha implementação foi de: "+ str(precisaok1) + " do sklearn foi: " + str(precisaoskk1))
print("A revocação para k=1 da minha implementação foi de: " + str(revocacaok1) + " do sklearn foi: " + str(revocacaoskk1))

print("A acuracia para k=3 da minha implementação foi de: " + str(acuraciak3) + " do sklearn foi: " + str(acuraciaskk3))
print("A precisao para k=3 da minha implementação foi de: "+ str(precisaok3) + " do sklearn foi: " + str(precisaoskk3))
print("A revocação para k=3 da minha implementação foi de: " + str(revocacaok3) + " do sklearn foi: " + str(revocacaoskk3))


print("A acuracia para k=5 da minha implementação foi de: " + str(acuraciak5) + " do sklearn foi: " + str(acuraciaskk5))
print("A precisao para k=5 da minha implementação foi de: "+ str(precisaok5) + " do sklearn foi: " + str(precisaoskk5))
print("A revocação para k=5 da minha implementação foi de: " + str(revocacaok5) + " do sklearn foi: " + str(revocacaoskk5))

print("A acuracia para k=7 da minha implementação foi de: " + str(acuraciak7) + " do sklearn foi: " + str(acuraciaskk7))
print("A precisao para k=7 da minha implementação foi de: "+ str(precisaok7) + " do sklearn foi: " + str(precisaoskk7))
print("A revocação para k=7 da minha implementação foi de: " + str(revocacaok7) + " do sklearn foi: " + str(revocacaoskk7))
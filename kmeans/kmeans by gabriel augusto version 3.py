import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from ucimlrepo import fetch_ucirepo 
import sys
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import random
import os
os.environ["LOKY_MAX_CPU_COUNT"] = "2" 

# fetch dataset 
iris = fetch_ucirepo(id=53) 
  
todasasmedidas= iris.data.features 
todasclassificacoes = iris.data.targets 

vetortodasmedidas = []
for i in range(0, len(todasasmedidas)):
    vetortodasmedidas.append(todasasmedidas.iloc[i])


#calcula a distancia euclidiana de n dimencoes entre a e b
def distanciaEuclidiana(a, b):
    soma = 0
    for i in range(0, len(a)):
        soma += (a[i] - b[i])**2
    return soma**(0.5)

#compara dois vetores de posições iguais
def comparaCentroids(centroidA, centroidB):
    for i in range(0, len(centroidA)):
        for j in range (0, len(centroidA[0])):
            if (centroidA[i][j]!= centroidB[i][j]):
                return False
    return True

#Retorna um vetor com k clusters de n atributos do arranjo
def kmeans(k, arranjo, contador, centroidsatuais, centroidantigos):
    #se nenhum centroid inicial foi passado, sorteia os centroids
    if(centroidsatuais == None):
        centroidsatuais = []
        i = 0
        while (i<k):
            #centroidsatuais.append(vetortodasmedidas[i*( int(len(vetortodasmedidas)/k))])
            limiteInferior = i*( int(len(vetortodasmedidas)/k))
            limiteSuperior = ((i+1)*( int(len(vetortodasmedidas)/k)))-1
            centroidsatuais.append(vetortodasmedidas[random.randint(limiteInferior, limiteSuperior)])
            i+=1
        print("sorteou centroids")
    
    for i in range (0, k):
        print("centroidatual "+str(i)+" "+str(centroidsatuais[i][0])+" "+str(centroidsatuais[i][1])+" "+str(centroidsatuais[i][2])+" "+str(centroidsatuais[i][3]))
    grupos = []

    #cria um vetor de amostras pros k clusters
    for i in range (0, k):
        grupos.append([])

    #calcula a distancia de cada elemento do arranjo o alocando pra um cluster
    for i in range(0, len(arranjo)):
        pertenceaokcentroid = -1
        distanciamenor = sys.float_info.max

        x=0
        while(x<k):
            distancia = distanciaEuclidiana(centroidsatuais[x], arranjo[i])
            if( distancia < distanciamenor):
                distanciamenor = distancia
                pertenceaokcentroid = x
            x+=1
        grupos[pertenceaokcentroid].append(arranjo[i])

    #cria vetor dos novos centroids
    novocentroid = []
    for i in range(0, len(centroidsatuais)):
        novocentroid.append([])
        for j in range(len(centroidsatuais[0])):
            novocentroid[i].append(0)

    #calcula os novos centroids
    for i in range (0, len(novocentroid)):
        soma = [0]*4
        print(len(grupos[i]))
        for j in range (0, len(grupos[i])):
            for l in range (0, len(todasasmedidas.iloc[0])):
                soma[l]+= (grupos[i][j][l]/(len(grupos[i])))

            for l in range(0, len(soma)):
                novocentroid[i][l] = soma[l]

    for i in range(0, len(novocentroid)):
        print("novo centroid " +str(i)+" "+ str(novocentroid[i][0])+" "+str(novocentroid[i][1])+" "+str(novocentroid[i][2])+ " "+ str(novocentroid[i][3]))
    
    #testa se o centroid convergiu retorna o novocentroid, se nao, chama o kmeans recursivamente até convergir
    if(centroidantigos!= None and comparaCentroids(novocentroid,centroidsatuais)): #comparaCentroids(novocentroid, centroidsatuais)):
        print("convergiu")
        return novocentroid
    else:
        print("Não convergiu")
        if (centroidantigos==None or (not comparaCentroids(novocentroid,centroidsatuais))):
            return kmeans(k, arranjo, contador, novocentroid, centroidsatuais)
        elif(comparaCentroids(novocentroid, centroidantigos)):
            if(contador<10):
                contador+=1
                return kmeans(k, arranjo, contador, novocentroid, centroidsatuais)
            else:
                return novocentroid


#função que dado um arranjo e um arranjo de centroids, plota os elementos do arranjo para os k centroids passados
def plotClusters( arranjo, centroids):
    novosTargets = []
    vetorX= []
    vetorY = []
    for i in range (0, len(arranjo)):
        vetorX.append(arranjo[i][0])
        vetorY.append(arranjo[i][1])
        distanciamenor = sys.float_info.max
        targetvalue = -1
        for j in range(0, len(centroids)):
            distancia= distanciaEuclidiana(arranjo[i], centroids[j])
            if(distancia < distanciamenor):
                distanciamenor= distancia
                targetvalue = j
        novosTargets.append(targetvalue)
    
    plt.scatter(vetorX, vetorY, c=novosTargets, cmap=plt.cm.Set1, edgecolor='k')
    titulo = "Iris dataset with k="+ str(len(centroids))+ " means (implementação propria) com " 
    titulo+= str(silhouette_score(vetortodasmedidas, novosTargets).round(3)) +" de silhouette score"
    plt.title(titulo)
    plt.show()

#executando pra implementação da dupla o k=3 e k=5, no final mostra um grafico com a distribuição dos k centroids e no titulo
#o silhouette score
k = 3
while (k <=5):
    centroids = kmeans(k, vetortodasmedidas, 0, None, None)
    plotClusters(vetortodasmedidas, centroids)
    k+=2

#executando pra implementação do sklearn o k=3 e k=5, no final mostra um grafico com a distribuição dos k centroids e no titulo
#o silhouette score
k =3
while (k <=5):
    skkmeans = KMeans(n_clusters=k,  init='k-means++')
    sktargets = skkmeans.fit_predict(vetortodasmedidas)
    vetorX= []
    vetorY = []
    for i in range (0, len(vetortodasmedidas)):
        vetorX.append(vetortodasmedidas[i][0])
        vetorY.append(vetortodasmedidas[i][1])
    plt.scatter(vetorX, vetorY, c=sktargets, cmap=plt.cm.Set1, edgecolor='k')
    titulo = "Iris dataset with k="+ str(k)+ " means (implementação sklearn) com " 
    titulo+= str(silhouette_score(vetortodasmedidas, sktargets).round(3)) +" de silhouette score"
    plt.title(titulo)
    plt.show()
    k+=2
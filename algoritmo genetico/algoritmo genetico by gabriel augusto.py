import random
import copy
import sys

#função que fornece o nverso de um bit
def inverso( bit):
    if bit == 1:
        return 0
    return 1

#funcao que inverte os bits de um vetor
def inverteBits (vetor):
    aux = [0, 0, 0, 0, 0]
    for i in range (0, len(vetor)):
        aux[i] = inverso(vetor[i])
    return aux

#funcao que soma um a um numero binario
def somaUm( vetor):
    somando = 1
    i = len(vetor)-1
    while i >=0:
        if( vetor[i]==0):
            vetor[i]=somando
            somando =0
        if(vetor[i]+somando==2):
            vetor[i]=0
        else:
            i=-1
        i=i-1
    return vetor

#funcao que faz o complemento de dois, pra fornecer a forma binaria de um numero decimal negativo
def complementoDeDois (vetor):
    aux = inverteBits(vetor)
    return somaUm(aux)

#funcao que retorna a forma decimal de um numero binario
def converteBinarioPraDecimal (vetor):
    #print(vetor)
    numeroNegativo = False
    aux = vetor

    if vetor[0]==1:
        numeroNegativo= True
        aux = complementoDeDois(vetor)
    
    i = len(vetor)-1
    potenciaDeDois=1
    valor=0

    while i>0:
        valor+=aux[i]*potenciaDeDois
        potenciaDeDois*=2
        i= i-1

    if numeroNegativo:
        return valor*(-1)
    
    return valor

#funcao que retorna um vetor representando a forma binaria de um numero decimal
def converteDecimalParaBinario (valor):
    #print("valor "+ str(valor))
    retorno = [0, 0, 0, 0, 0]
    countBit = len(retorno)-1
    flagNegativo = valor<0
    while countBit>=1:
        #print("valor%2 "+ str(valor%2))
        retorno[countBit]= valor%2
        #print("valor/2" + str(valor/2))
        valor= int(valor/2)
        countBit= countBit-1
    if(flagNegativo):
        return complementoDeDois(retorno)
    return retorno
#print(converteDecimalParaBinario(-10))
#print(converteDecimalParaBinario(10))

#funcao que retorna uma matriz com tamanhoPopulacao numeros binarios (cada linha é um numero, cada coluna um bit)
def geraPopulacao (tamanhoPopulacao):
    count =0
    numerosAdicionados = set()
    retorno = []
    while count< tamanhoPopulacao and count < 21:
        aleatorio = random.randint(-10, 10)
        if not (aleatorio in numerosAdicionados):
            print("Adicionando "+ str(aleatorio) +" a populacao inicial")
            numerosAdicionados.add(aleatorio)
            retorno.append( converteDecimalParaBinario(aleatorio))
            count=count+1
    while tamanhoPopulacao>=21 and count < tamanhoPopulacao:
        aleatorio = random.randint(-10, 10)
        retorno.append(converteDecimalParaBinario(aleatorio))
        count= count+1
    return retorno

#funcao que faz o crossover entre dois individuos
def crossOver( individuo1, individuo2, taxaCrossOver):
    #se o cross over é selecionado continua a funcao
    rollChance = random.randint(1,100)
    if rollChance <= taxaCrossOver:
        crossOverValido = False
        tentativa = 0
        #crossOverValido é para verificar se o crossOver resultante nao viola o dominio da  ([-10,10])
        while not crossOverValido and tentativa<15:
            rollPosition = random.randint(1, len(individuo1)-2)
            copiaIndividuo1 = copy.deepcopy(individuo1)
            copiaIndividuo2 = copy.deepcopy(individuo2)
            i = len(individuo1)-1
            #faz o cross over da rollPosition posicao pra frente, rollPosition nao pode ser 0 nem ultima posicao do vetor
            while i > rollPosition:
                individuo1[i] = copiaIndividuo2[i]
                individuo2[i] = copiaIndividuo1[i]
                i= i-1
            if ( converteBinarioPraDecimal(individuo1) <=10 and converteBinarioPraDecimal(individuo1) >=-10 ):
                if(converteBinarioPraDecimal(individuo2)<=10 and  converteBinarioPraDecimal(individuo2)>= -10):
                    crossOverValido= True
                    print("CrossOver selecionado em " + str(rollPosition))
                    print("Individuos anteriores:\t"+ str(copiaIndividuo1)+"\t"+str(copiaIndividuo2))
                    print("Individuos novos:\t"+ str(individuo1)+ "\t" + str(individuo2))
                    return True
            j=0
            #se o crossOver violou o dominio, tenta novamente outro crossOver
            while j< len(copiaIndividuo1) and not crossOverValido:
                individuo1[j] = copiaIndividuo1[j]
                individuo2[j] = copiaIndividuo2[j]
                j+=1
            tentativa +=1
    return False

#funcao que pode mutar individuos, um aleatorio é sorteado para cada bit (alelo), se cai na chance de mutacao, entao inverte o bit selecionado
#0 ou varios bits podem ser mutados (todos os alelos do cromossomo estao sujeitos), no fim verifica se a mutacao nao violou o dominio da funcão
def mutacao (individuo, taxaMutacao):
    i =1 
    individuoAntes = copy.deepcopy(individuo)
    houveMutacao = False
    while i < len(individuo):
        rollChance = random.randint(1,100)
        if(rollChance<= taxaMutacao):
            houveMutacao=True
            individuo[i]= inverso(individuo[i])
        i+=1
    
    if(converteBinarioPraDecimal(individuo)>10 or converteBinarioPraDecimal(individuo)< -10):
        for i in range (0, len(individuo)):
            individuo[i] = individuoAntes[i]
        return mutacao(individuo, taxaMutacao)
    
    if houveMutacao:
        print("Houve mutacao, o individuo era\t"+ str(individuoAntes)+ " e se tornou\t"+ str(individuo))
    return

#funcao que avalia quao bem um individuo é adaptado ao problema, valores maiores são desejados
#segue a formula descrita na descrição do trabalho
def fitness1 (individuo):
    valorIndividuo = converteBinarioPraDecimal (individuo)
    return (valorIndividuo**2)- (3*valorIndividuo) + 4

def fitness2 (individuo):
    valorIndividuo = converteBinarioPraDecimal (individuo)
    return (valorIndividuo**2)- (3*individuo) + 4

def fitness3 (individuo):
    valorIndividuo = converteBinarioPraDecimal (individuo)
    return (valorIndividuo**2)- (3*individuo) + 4

#funcao que faz o torneio baseado na formula da descrição do trabalho
def torneio1(individuo1, individuo2):
    if fitness1(individuo1)> fitness1(individuo2):
        return individuo1
    return individuo2

#print(torneio1([0, 0, 0, 0, 1], [0, 0, 0, 1, 0]))

#funcao principal de execucao do algoritmo genetico, a saida é a populacao adaptada após numGEracoes iteracoes
def algoritmoGenetico1(tamanhoPopulacao, taxaCrossOver, taxaMutacao, numGeracoes):
    #contador da iteracao
    countGeracao =0
    #populacao inicial é aleatória
    populacao = geraPopulacao(tamanhoPopulacao)
    print("primeira geracao")
    print(populacao)
    while countGeracao < numGeracoes:
        #inicio de uma nova geracao
        novaGeracao = []
        count =0
        #a cada iteracao do loop a seguir um novo individuo da nova geracao é gerado
        while count < tamanhoPopulacao:
            #sorteia dois individuos
            pos1 = random.randint(0, tamanhoPopulacao-1)
            pos2 = random.randint(0, tamanhoPopulacao-1)
            #loop para forcar escolher dois individuos diferentes para realização do torneio
            while pos1==pos2:
                pos2 = random.randint(0, tamanhoPopulacao-1)
            #print("pos1 " + str(pos1))
            #print("pos2 " + str(pos2))
            
            #realiza torneio
            novoIndividuo = copy.deepcopy(torneio1( populacao[pos1], populacao[pos2]))
            #mutacao(novoIndividuo, taxaMutacao)
            novaGeracao.append(novoIndividuo)
            #se ja escolheu dois individuos, chama a funcao que decide se faz cross over ou nao
            if(count%2==1):
                crossOver( novaGeracao[count-1], novaGeracao[count], taxaCrossOver)
                #chama a funcao que faz mutacao ou nao
                mutacao( novaGeracao[count], taxaMutacao)
                mutacao( novaGeracao[count-1], taxaMutacao)
            else:
                mutacao(novaGeracao[count], taxaMutacao)
            count+=1
        countGeracao+=1
        populacao = novaGeracao
        print("nova populcao é:")
        for linha in populacao:
            print(str(linha)+" ( "+ str(converteBinarioPraDecimal(linha))+ " )")
    #no final retorna a populacao adaptada em numGeracoes iteracoes
    return populacao

#seleciona melhor individuo da geracao
def melhorDaGeracao( populacao):
    i =0
    posMaior = -1
    valorMaior = -sys.maxsize
    #print("populacao no melhordageracao")
    #print(populacao)
    for linha in populacao:
        valor =fitness1(linha)
        if valor > valorMaior:
            valorMaior = valor
            posMaior =i
        i= i+1
    return (populacao[posMaior], valorMaior)

continuarTestando = True
while continuarTestando:
    print("Testando algoritmo genetico")
    tamanhoPopulacao = int(input("Digite o tamanho da populacao [4, 30]: "))
    #tamanhoPopulacao = int(tamanhoPopulacao)
    if tamanhoPopulacao < 4:
        tamanhoPopulacao=4
    elif tamanhoPopulacao >30:
        tamanhoPopulacao=30
    taxaMutacao = int(input("Digite a taxa de mutacao [0, 100], recomendado valores menores que 5: "))
    if taxaMutacao<0 or taxaMutacao > 100:
        taxaMutacao= 1
    taxaCrossOver = int(input("Digite a taxa de Cross Over [0, 100], recomendado 70: "))
    if taxaCrossOver <0 or taxaCrossOver>100:
        taxaCrossOver = 70
    numGeracoes = int(input("Digite o numero de geracoes [5, 20]: "))
    if numGeracoes <5 or numGeracoes > 20:
        numGeracoes = 5
    resultado = melhorDaGeracao(algoritmoGenetico1(tamanhoPopulacao, taxaCrossOver, taxaMutacao, numGeracoes))
    print("Melhor individuo foi: " + str(resultado[0]) +" em binario que é "+ str(converteBinarioPraDecimal(resultado[0])) + " decimal")
    print("Resultando no valor de "+ str(resultado[1]))
    
    pergunta = input("Deseja testar novamente? (s or n): ")
    if pergunta == 'n':
        continuarTestando= False
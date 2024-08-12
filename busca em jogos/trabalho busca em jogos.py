import random
from collections import deque
import copy

#cria uma nova matriz, e faz a troca de elementos e retorna a nova matriz com os elementos trocados
def swap (x1, y1, x2, y2, matriz):
    #print ("x1: "+ str(x1), " y1: "+ str(y1), " x2: "+ str(x2)+ " y2: "+str(y2))
    retorno = copy.deepcopy(matriz)
    a = retorno[x1][y1]
    retorno [x1][y1]= retorno[x2][y2]
    retorno[x2][y2]=a
    return retorno

#verifica se o movimento é valido
def verificaMovimento (movimento, matriz, x1, y1):
    if(matriz[x1][y1]==None):
        if movimento == "cima":
            if x1-1>=0:
                return True
        if movimento == "baixo":
            if x1+1<=2:
                return True
        if movimento == "esquerda":
            if y1-1>=0:
                return True
        if movimento == "direita":
            if y1+1<=2:
                return True
    return False

#realiza o movimento
def movimento (movimento, matriz, x, y):
    if movimento == "cima":
        return swap (x, y, x+1, y, matriz)
    if movimento == "baixo":
        return swap (x, y, x-1, y, matriz)
    if movimento == "esquerda":
        return swap (x, y, x, y+1, matriz)
    if movimento == "direita":
        return swap (x, y, x, y-1, matriz)
    
#verifica se o jogo está na posicao correta (vitoria)
def verificaVitoria(matriz):
    if(matriz[0][0]==1 and matriz[0][1]==2 and matriz[0][2]==3):
        if(matriz[1][0]==8 and matriz[1][1]== None and matriz[1][2]==4):
            if(matriz[2][0]==7 and matriz[2][1]==6 and matriz[2][2]==5):
                return True
    return False

#retorna tupla com as coordenadas da casa vazia (None)
def posicaoVazia( matriz):
    for i in range(len(matriz)):
        for j in range (len(matriz[i])):
            if matriz[i][j]== None:
                return (i, j)

#gera um jogo aleatorio, a posicao dos numeros é aleatória e a posicao vazia também
def geraJogo():
    jogo = []
    for i in range (0,3):
        linha = []
        for j in range (0,3):
            linha.append(-1)
        jogo.append(linha)

    xvazio = random.randint(0,2)
    yvazio = random.randint(0,2)
    jogo[xvazio][yvazio]= None

    numeros = list(range(1, 9))
    random.shuffle(numeros)
    index = 0
    for i in range(3):
        for j in range(3):
            if jogo[i][j]!=None:
                jogo[i][j] = numeros[index]
                index += 1
    return jogo


contSemHeuristica =0
#resolve o jogo usando uma busca em largura
def resolveSemHeuristica(jogo):
    #cria fila de estados, um estado é uma tupla com (estado atual, movimento anterior, fila de estados da arvore que chegou o estado atual)
    filaEstados = deque()
    filaEstados.append( (jogo,  None, [jogo]) )
    vitoria = False #flag para o loop
    count =0        #contador para evitar estouro de memoria
    while (not vitoria) and count<5000:
        estado = filaEstados.popleft()  #desinfilera
        if (verificaVitoria(estado[0])): #verifica vitoria, se ganhou imprime os jogadas que levam a vitoria
            vitoria = True
            print("sequencia de jogadas para vencer sem heuristica:")
            for e in estado[2]:
                for i in range(len(e)):
                    print(str(e[i][0])+ "\t"+ str(e[i][1])+ "\t"+ str(e[i][2])+ "\n")
                print("->")
            print("Foram necessarias "+ str(count)+ " iteracoes para vencer sem heuristica")
            global contSemHeuristica
            contSemHeuristica= count
            return True
        else: #se nao ganhou, olha proximos estados possiveis e os enfileira na fila de estados
            #print(estado[1])    #mostra movimento anterior
            #for i in range (len(estado[0])):    #imprime estado atual
                #print( str(estado[0][i][0])+"\t"+ str(estado[0][i][1]) + "\t" + str(estado[0][i][2])+ "\n")
            #print(count)

            posicao = posicaoVazia(estado[0]) #descobre posicao vazia, usado para fazer os outros movimentos
            #faz movimentos possiveis sempre seguindo essa ordem: cima, baixo, esquerda, direita
            if verificaMovimento("cima" ,estado[0], posicao[0], posicao[1]) and (estado[1]!="baixo"): #verifica se o movimento é valido
                copiaMatriz = copy.deepcopy(estado[0])  #copia matriz
                novaMatriz = movimento("cima",copiaMatriz, posicao[0]-1, posicao[1]) #faz movimento
                novaLista = copy.deepcopy( estado[2])   #copia braço da arvore dee jogadas
                novaLista.append(novaMatriz)    #adiciona nova jogada
                filaEstados.append( (novaMatriz, "cima", novaLista ) ) #adiciona novo estado na fila

            #mesmo procedimento pra outras jogadas possiveis
            if verificaMovimento("baixo" ,estado[0],posicao[0], posicao[1]) and (estado[1]!="cima"):
                copiaMatriz = copy.deepcopy(estado[0])
                novaMatriz = movimento("baixo",copiaMatriz, posicao[0]+1, posicao[1])
                novaLista = copy.deepcopy( estado[2])
                novaLista.append(novaMatriz) 
                filaEstados.append( (novaMatriz, "baixo", novaLista ) )

            if verificaMovimento("esquerda" ,estado[0],posicao[0], posicao[1]) and (estado[1]!="direita"):
                copiaMatriz = copy.deepcopy(estado[0])
                novaMatriz = movimento("esquerda",copiaMatriz, posicao[0], posicao[1]-1)
                novaLista = copy.deepcopy( estado[2])
                novaLista.append(novaMatriz) 
                filaEstados.append( (novaMatriz, "esquerda", novaLista ) )

            if verificaMovimento("direita" ,estado[0], posicao[0], posicao[1]) and (estado[1]!="esquerda"):
                copiaMatriz = copy.deepcopy(estado[0])
                novaMatriz = movimento("direita",copiaMatriz, posicao[0], posicao[1]+1)
                novaLista = copy.deepcopy( estado[2])
                novaLista.append(novaMatriz) 
                filaEstados.append( (novaMatriz, "direita", novaLista) )
        count+=1
    if count>=5000:
        print("Infelizmente 5000 iteracoes nao foram suficientes sem heuristica, tentando com heuristica")
        contSemHeuristica=-1
    return False

def pecaNoLugarCerto( peca, x, y):  #função que verifica se a peça peca está na posicao correta
    if peca == 1 and x==0 and y==0:
        return True
    if peca ==2 and x==0 and y==1:
        return True
    if peca == 3 and x==0 and y==2:
        return True
    if peca == 4 and x==1 and y==2:
        return True
    if peca == 5 and x==2 and y==2:
        return True
    if peca == 6 and x==2 and y==1:
        return True
    if peca ==7 and x==2 and y==0:
        return True
    if peca==8 and x==1 and y==0:
        return True
    return False

def lugarOtimo(matriz, x, y, movimento):    #funcao usada na hora de determinar prioridades
    mov = movimentoContrario(movimento)     #olha se a peca está no lugar certo
    novoX = x+ mov[1]
    novoY = y+ mov[2]
    #print (str(matriz[x][y])+" x: "+ str(x)+ " y: "+ str(x))
    if pecaNoLugarCerto(matriz[novoX][novoY], novoX, novoY):
        return True
    return False

def movimentoContrario( inverter):      #funcao que retorna o movimento e valores contrarios de inverter
    if inverter == "cima":
        return ("baixo", 1, 0)
    if inverter == "baixo":
        return ("cima", -1, 0)
    if inverter == "esquerda":
        return ("direita", 0, 1)
    if inverter =="direita":
        return ("esquerda", 0, -1)
    return None

def lugarRuim(matriz, movimentoAtual, x, y):        #funcao que verifica se o movimento feito foi um movimento que tirou a peca do lugar certo
    movimentoAnterior = movimentoContrario(movimentoAtual)
    #print(x)
    #print(y)
    #print(movimentoAnterior)
    novoX =x+ movimentoAnterior[1]
    novoY = y+movimentoAnterior[2]
    #print(novoX)
    #print(novoY)
    #print(matriz[novoX][novoY])
    inverteuCerto = pecaNoLugarCerto(matriz[novoX][novoY], x , y )
    #print("Esta no lugar certo " + str(inverteuCerto))
    if(inverteuCerto):
        return True
    return False

def prioridadeDoMovimento( matriz, movimento, x, y):    #funcao que retorna a prioridade
    if lugarOtimo(matriz, x, y, movimento): #jogadas que colocam as pecas no lugar certo tem prioridade
        return 1
    elif lugarRuim(matriz, movimento, x, y):    #jogadas que tiram as pecas de seu lugar correto tem a menor prioridade
        return 3
    else:
        return 2    #jogada que nao eh boa nem ruim

contComHeuristica = 0
def resolveComHeuristica (jogo):
    #cria fila de estados, um estado é uma tupla com (estado atual, movimento anterior, fila de estados da arvore que chegou o estado atual)
    filaEstados = deque()
    filaEstados.append( (jogo,  None, [jogo]) )
    vitoria = False #flag para o loop
    count =0        #contador para evitar estouro de memoria
    while (not vitoria) and count<5000:
        estado = filaEstados.popleft()  #desinfilera
        if (verificaVitoria(estado[0])): #verifica vitoria, se ganhou imprime os jogadas que levam a vitoria
            vitoria = True
            print("sequencia de jogadas para vencer usando heuristica:")
            for e in estado[2]:
                for i in range(len(e)):
                    print(str(e[i][0])+ "\t"+ str(e[i][1])+ "\t"+ str(e[i][2])+ "\n")
                print("->")
            print("Foram necessarias "+ str(count)+ " iteracoes para vencer com heuristica")
            global contComHeuristica
            contComHeuristica=count
            return True
        else: #se nao ganhou, olha proximos estados possiveis e os enfileira na fila de estados
            #print(estado[1])    #mostra movimento anterior
            #for i in range (len(estado[0])):    #imprime estado atual
                #print( str(estado[0][i][0])+"\t"+ str(estado[0][i][1]) + "\t" + str(estado[0][i][2])+ "\n")
            #print(count)

            primeiraFileDeEstados = deque()
            segundaFilaDeEstados = deque()
            terceiraFilaDeEstados = deque()
            posicao = posicaoVazia(estado[0]) #descobre posicao vazia, usado para fazer os outros movimentos
            #faz movimentos possiveis sempre seguindo essa ordem: cima, baixo, esquerda, direita
            if verificaMovimento("cima" ,estado[0], posicao[0], posicao[1]) and (estado[1]!="baixo"): #verifica se o movimento é valido
                copiaMatriz = copy.deepcopy(estado[0])  #copia matriz
                novaMatriz = movimento("cima",copiaMatriz, posicao[0]-1, posicao[1]) #faz movimento
                prioridade = prioridadeDoMovimento(novaMatriz, "cima", posicao[0]-1, posicao[1]) #determina prioridade do movimento
                novaLista = copy.deepcopy( estado[2])   #copia braço da arvore dee jogadas
                novaLista.append(novaMatriz)    #adiciona nova jogada
                #print("cima "+ str(prioridade))
                if(prioridade == 1):    #coloca em filas diferentes de acordo com a prioridade
                    primeiraFileDeEstados.append( (novaMatriz, "cima", novaLista ) )
                elif(prioridade == 2):
                    segundaFilaDeEstados.append( (novaMatriz, "cima", novaLista ))
                else:
                    terceiraFilaDeEstados.append( (novaMatriz, "cima", novaLista ))

            #mesmo procedimento pra outras jogadas possiveis
            if verificaMovimento("baixo" ,estado[0],posicao[0], posicao[1]) and (estado[1]!="cima"):
                copiaMatriz = copy.deepcopy(estado[0])
                
                novaMatriz = movimento("baixo",copiaMatriz, posicao[0]+1, posicao[1])
                prioridade = prioridadeDoMovimento(novaMatriz, "baixo", posicao[0]+1, posicao[1])
                novaLista = copy.deepcopy( estado[2])
                novaLista.append(novaMatriz) 

                #print("baixo "+ str(prioridade))
                if prioridade == 1:
                    primeiraFileDeEstados.append( (novaMatriz, "baixo", novaLista ) )
                elif prioridade == 2:
                    segundaFilaDeEstados.append( (novaMatriz, "baixo", novaLista ))
                else:
                    terceiraFilaDeEstados.append( (novaMatriz, "baixo", novaLista ))

            if verificaMovimento("esquerda" ,estado[0],posicao[0], posicao[1]) and (estado[1]!="direita"):
                copiaMatriz = copy.deepcopy(estado[0])
                novaMatriz = movimento("esquerda",copiaMatriz, posicao[0], posicao[1]-1)
                prioridade = prioridadeDoMovimento(novaMatriz, "esquerda", posicao[0], posicao[1]-1)
                novaLista = copy.deepcopy( estado[2])
                novaLista.append(novaMatriz) 

                #print("esquerda "+ str(prioridade))
                if prioridade == 1:
                    primeiraFileDeEstados.append( (novaMatriz, "esquerda", novaLista ) )
                elif prioridade == 2:
                    segundaFilaDeEstados.append( (novaMatriz, "esquerda", novaLista ) )
                else:
                    terceiraFilaDeEstados.append( (novaMatriz, "esquerda", novaLista ) )

            if verificaMovimento("direita" ,estado[0], posicao[0], posicao[1]) and (estado[1]!="esquerda"):
                copiaMatriz = copy.deepcopy(estado[0])
                novaMatriz = movimento("direita",copiaMatriz, posicao[0], posicao[1]+1)
                prioridade = prioridadeDoMovimento(novaMatriz, "direita", posicao[0], posicao[1]+1)
                novaLista = copy.deepcopy( estado[2])
                novaLista.append(novaMatriz) 

                #print("direita "+ str(prioridade))
                if prioridade == 1:
                    primeiraFileDeEstados.append( (novaMatriz, "direita", novaLista)  )
                elif prioridade == 2:
                    segundaFilaDeEstados.append( (novaMatriz, "direita", novaLista)  )
                else:
                    terceiraFilaDeEstados.append( (novaMatriz, "direita", novaLista)  )
            

            for e in primeiraFileDeEstados: #movimentos prioritarios serao explorados primeiro
                filaEstados.append(e)
            for e in segundaFilaDeEstados:  #movimentos neutros serão explorado depois dos primeiros
                filaEstados.append(e)
            for e in terceiraFilaDeEstados: #movimentos ruins são explorados por ultimo
                filaEstados.append(e)
            count+=1

    if count>=5000:
        print("Infelizmente 5000 iteracoes nao foram suficientes para resolver com heuristica, gerando outro jogo")
        contComHeuristica=-1
    return False

def jogar():
    naoVenceu = True
    while( naoVenceu):
        jogo = geraJogo()

        for linha in jogo:
            print(linha)

        print("Resolvendo sem heuristicas, por favor espere, o programa tentara 5000 iteracoes para resolver")
        semHeuristica = resolveSemHeuristica(jogo)
        print("Resolvendo com heuristicas, por favor espere, o programa tentara 5000 iteracoes para resolver")
        comHeuristica = resolveComHeuristica(jogo)
        if(comHeuristica or semHeuristica):
            naoVenceu = False

    print("Sem heuristica foram necessarias "+ str(contSemHeuristica) +" iteracoes")
    print("Com heuristica foram necessariass "+ str(contComHeuristica)+ " iteracoes")
    print("Se o resultado for -1, significa que as 5000 iteracoes do metodo nao foram suficientes")
jogar()

from tabulate import tabulate



file = open("../TPC1/myheart.csv", "rt")
content = file.read()

#lista de strings com todas as linhas do ficheiro csv
lista_linhas = content.splitlines()[1:]

file.close()

#função que recebe um lista de strings e retorna uma lista com dicionários em 
#que cada dicionário corresponde a informações de uma pessoa
def parse(lista_linhas):
    lista_dics = []
    for line in lista_linhas:
        idade,sexo,tensao,colesterol,batimento,temDoenca = line.split(',')
        dic = dict()
        dic["idade"]      = int(idade)
        dic["sexo"]       = sexo
        dic["tensao"]     = int(tensao)
        dic["colesterol"] = int(colesterol)
        dic["batimento"]  = int(batimento)
        dic["temDoenca"]  = bool(int(temDoenca))
        lista_dics.append(dic)
    return lista_dics

lista_info=parse(lista_linhas)


#--------------------------------- Exercício 1 -------------------------------------
#função que recebe uma lista de dicionarios e devolve um dicionario com duas chaves 
#("M", "F") em que cada valor corresponde ao número de doentes desse sexo

def doencas_por_sexo(lista):
    dict_doencas_por_sexo = {'M':0,'F':0}
    for dict in lista:
        if(dict["temDoenca"]==1):
            if(dict["sexo"]=='M'):
                dict_doencas_por_sexo["M"]+=1 
            elif(dict["sexo"]=='F'):
                dict_doencas_por_sexo["F"]+=1
    return dict_doencas_por_sexo

doencas_sexo= doencas_por_sexo(lista_info)
#print(doencas_sexo)


#---------------------------------- Exercício 2 ------------------------------------
#Calcular distribuição de doenças por escalões etários
#primeiro calculei a pessoa mais nova e mais velha do dataset para saber aonde começar terminar o intervalo 
#depois tem duas funções, uma que da a possíbilidade de escolha de idade e outra que já tem por default

def pessoa_mais_velha(lista):
    maior_idade = -1
    for dict in lista:
        if(dict["idade"]>=maior_idade):
            maior_idade=dict["idade"]
    return int(maior_idade)

maior_idade = pessoa_mais_velha(lista_info)
#print(maior_idade)

def pessoa_mais_nova(lista):
    menor_idade = maior_idade
    for dict in lista:
        if(dict["idade"]<=menor_idade):
            menor_idade=dict["idade"]
    return int(menor_idade)

menor_idade = pessoa_mais_nova(lista_info)
#print(menor_idade)

def doenca_por_intervalo_idade(lista, intervalo):
    dicionario_intervalo_idade = dict()
    limite_inf = menor_idade 
    limite_sup =0
    i = 0
    while(limite_sup<=maior_idade):
        limite_sup = limite_inf + intervalo
        dicionario_intervalo_idade[f"{limite_inf}-{limite_sup}"] = 0;
        limite_inf = limite_sup + 1
        i+=1
        
    for dic in lista:
        if(dic["temDoenca"]==1):
            idade = int(dic["idade"])
            for key in dicionario_intervalo_idade.keys():
                menor,maior = key.split("-")
                if(idade>=int(menor) and idade<=int(maior)):
                    dicionario_intervalo_idade[key] +=1
    return dicionario_intervalo_idade
            
l= doenca_por_intervalo_idade(lista_info,10)
#print(l)


def doenca_por_intervalo_idade(lista):
    intervalo = 5
    dicionario_intervalo_idade = dict()
    limite_inf = menor_idade
    limite_sup=0
    
    while(limite_sup<=maior_idade):
        limite_sup = limite_inf + intervalo
        dicionario_intervalo_idade[f"{limite_inf}-{limite_sup}"] = 0;
        limite_inf = limite_sup + 1
        
    for dic in lista:
        if(dic["temDoenca"]==1):
            idade = int(dic["idade"])
            for key in dicionario_intervalo_idade.keys():
                menor,maior = key.split("-")
                if(idade>=int(menor) and idade<=int(maior)):
                    dicionario_intervalo_idade[key] +=1
    return dicionario_intervalo_idade    
    
l= doenca_por_intervalo_idade(lista_info)
#print(l)


#---------------------------------- Exercício 3 ------------------------------------
#Calcular distribuição de doenças por distribuição da doença por níveis de colesterol. Considere um nível 
#igual a um intervalo de 10 unidades, comece no limite inferior e crie os níveis necessários até abranger o limite superior;

#primeiro calculei o nivel mais baixo e o mais alto do dataset para saber aonde começar terminar o intervalo 

def nivel_mais_alto(lista):
    maior_nivel = -1
    for dict in lista:
        if(dict["colesterol"]>=maior_nivel):
            maior_nivel=dict["colesterol"]
    return int(maior_nivel)

maior_nivel = nivel_mais_alto(lista_info)
print(maior_nivel)

def nivel_mais_baixo(lista):
    menor_nivel = maior_nivel
    for dict in lista:
        if(dict["colesterol"]<=menor_nivel):
            menor_nivel=dict["colesterol"]
    return int(menor_nivel)

menor_nivel = nivel_mais_baixo(lista_info)
print(menor_nivel)

def doenca_por_intervalo_colesterol(lista):
    intervalo = 10
    dicionario_intervalo_colesterol = dict()
    limite_inf = menor_nivel
    limite_sup=0
    
    while(limite_sup<=maior_nivel):
        limite_sup = limite_inf + intervalo
        dicionario_intervalo_colesterol[f"{limite_inf}-{limite_sup}"] = 0;
        limite_inf = limite_sup + 1
        
    for dic in lista:
        if(dic["temDoenca"]==1):
            idade = int(dic["colesterol"])
            for key in dicionario_intervalo_colesterol.keys():
                menor,maior = key.split("-")
                if(idade>=int(menor) and idade<=int(maior)):
                    dicionario_intervalo_colesterol[key] +=1
    return dicionario_intervalo_colesterol   
    
l= doenca_por_intervalo_colesterol(lista_info)
print(l)


#---------------------------------- Exercício 4 ------------------------------------

def tabular():
header = []
    #    return (tabulate(self.mat, headers = header, tablefmt = "grid"))
    
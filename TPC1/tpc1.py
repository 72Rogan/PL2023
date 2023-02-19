import sys
from tabulate import tabulate

#função que abre um ficheiro, le o seu conteudo
#coloca o conteudo numa lista de strings e retorna 
#uma lista com dicionários em que cada dicionário
#corresponde a informações de uma pessoa
def parse_file(diretoria):
    with open(diretoria, 'r') as file:
        content = file.read()
    lista_linhas = content.splitlines()[1:]
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

#--------------------------------- Exercício 1 -------------------------------------
#função que recebe uma lista de dicionarios e devolve um dicionario com duas chaves 
#("M", "F") em que cada valor corresponde ao número de doentes desse sexo

def doencas_por_sexo(lista):
    dict_doencas_por_sexo = {'M':(0,0),'F':(0,0)}
    for dict in lista:
        if(dict['sexo'].upper() == "M"):
            dict_doencas_por_sexo["M"]=(dict_doencas_por_sexo["M"][0],dict_doencas_por_sexo["M"][1]+1)
            if(dict["temDoenca"]==1):
                dict_doencas_por_sexo["M"]=(dict_doencas_por_sexo["M"][0]+1,dict_doencas_por_sexo["M"][1]) 
        elif(dict["sexo"]=='F'):
            dict_doencas_por_sexo["F"]=(dict_doencas_por_sexo["F"][0],dict_doencas_por_sexo["F"][1]+1)
            if(dict["temDoenca"]==1):
                dict_doencas_por_sexo["F"] = (dict_doencas_por_sexo["F"][0]+1,dict_doencas_por_sexo["F"][1])
    return dict_doencas_por_sexo

def print_doencas_por_sexo(dic):
    (homens_doentes,homens_total) = dic["M"]
    (mulheres_doentes,mulheres_total) = dic["F"]
    print(f"{homens_doentes} homens doentes em {homens_total} homens ---> {(homens_doentes / homens_total)*100}%")
    print(f"{mulheres_doentes} mulheres doentes em {mulheres_total} mulheres ---> {(mulheres_doentes/mulheres_total)*100}%")
    
    
#---------------------------------- Exercício 2 ------------------------------------
#Calcular distribuição de doenças por escalões etários
#primeiro calculei a pessoa mais nova e mais velha do dataset para saber aonde começar terminar o intervalo 
#depois tem duas funções, uma que da a possíbilidade de escolha de idade e outra que já tem por default

def pessoa_mais_velha(lista):
    maior_idade = lista[0]["idade"]
    for dict in lista:
        if(dict["idade"]>=maior_idade):
            maior_idade=dict["idade"]
    return int(maior_idade)

def pessoa_mais_nova(lista):
    menor_idade = lista[0]["idade"]
    for dict in lista:
        if(dict["idade"]<=menor_idade):
            menor_idade=dict["idade"]
    return int(menor_idade)


def doenca_por_intervalo_idade(lista,menor_idade,maior_idade,intervalo):
    dicionario_intervalo_idade = dict()
    limite_inf = menor_idade 
    limite_sup =0
    
    while(limite_sup<maior_idade):
        limite_sup = limite_inf + intervalo
        dicionario_intervalo_idade[f"{limite_inf}-{limite_sup}"] = (0,0);
        limite_inf = limite_sup + 1
   
    for dic in lista:
        idade = int(dic["idade"])
        for key in dicionario_intervalo_idade.keys():
                menor,maior = key.split("-")
                if(idade>=int(menor) and idade<=int(maior)):
                    dicionario_intervalo_idade[key] = (dicionario_intervalo_idade[key][0],dicionario_intervalo_idade[key][1]+1)
                    if(dic["temDoenca"]==1):
                        dicionario_intervalo_idade[key] = (dicionario_intervalo_idade[key][0]+1,dicionario_intervalo_idade[key][1])

    return dicionario_intervalo_idade
            

def doenca_por_intervaloDefault_idade(lista,menor_idade,maior_idade):
    intervalo = 5
    dicionario_intervalo_idade = dict()
    limite_inf = menor_idade
    limite_sup=0
    
    while(limite_sup<maior_idade):
        limite_sup = limite_inf + intervalo
        dicionario_intervalo_idade[f"{limite_inf}-{limite_sup}"] = (0,0);
        limite_inf = limite_sup + 1
        
    for dic in lista:
        idade = int(dic["idade"])
        for key in dicionario_intervalo_idade.keys():
                menor,maior = key.split("-")
                if(idade>=int(menor) and idade<=int(maior)):
                    dicionario_intervalo_idade[key] = (dicionario_intervalo_idade[key][0],dicionario_intervalo_idade[key][1]+1)
                    if(dic["temDoenca"]==1):
                        dicionario_intervalo_idade[key] = (dicionario_intervalo_idade[key][0]+1,dicionario_intervalo_idade[key][1])
    return dicionario_intervalo_idade    

def print_doenca_intervalo_idade(dic):
    for key in dic.keys():
        nDoentes = dic[key][0]
        nTotal = dic[key][1]
        print(f"Intervalo: {key} ---> {nDoentes} doentes em {nTotal} pessoas ---> {(nDoentes /nTotal)*100}%")
    

##---------------------------------- Exercício 3 ------------------------------------
##Calcular distribuição de doenças por distribuição da doença por níveis de colesterol. Considere um nível 
##igual a um intervalo de 10 unidades, comece no limite inferior e crie os níveis necessários até abranger o limite superior;
#
##primeiro calculei o nivel mais baixo e o mais alto do dataset para saber aonde começar terminar o intervalo 
#
def nivel_mais_alto(lista):
    maior_nivel = -1
    for dict in lista:
        if(dict["colesterol"]>=maior_nivel):
            maior_nivel=dict["colesterol"]
    return int(maior_nivel)

def nivel_mais_baixo(lista):
    menor_nivel = lista[0]["colesterol"]
    for dict in lista:
        if(dict["colesterol"]<=menor_nivel):
            menor_nivel=dict["colesterol"]
    return int(menor_nivel)

def doenca_por_intervalo_colesterol(lista,menor_nivel,maior_nivel):
    intervalo = 10
    dicionario_intervalo_colesterol = dict()
    limite_inf = menor_nivel
    limite_sup=0
    
    while(limite_sup<maior_nivel):
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

def print_colesterol(dic,nTotal):
    
    for key in dic.keys():
        print(f"Intervalo de colesterol: {key} ---> {dic[key]} pessoas em {nTotal} pessoas ---> {(dic[key] /nTotal)*100}%")


##---------------------------------- Exercício 4 ------------------------------------

def tabular(dic,escolha):
    table = []
    #1 - sexo : 2 - idade : 3 - colesterol
    if(escolha==1):
        headers = ['Sexo', 'Quantidade']
    if(escolha==2):
        headers = ['Intervalo idade', 'Quantidade']
    if(escolha==3):
        headers = ['Intervalo colesterol', 'Quantidade']

    for key in (dic.keys()):
            row = [key, dic[key]]
            table.append(row)
    print(tabulate(table, headers=headers))


def main():
    dir = "../TPC1/myheart.csv"
    lista = parse_file(sys.argv[1])
    
    dSexo = doencas_por_sexo(lista)
    print_doencas_por_sexo(dSexo)
    
    idadeMaisVelha = pessoa_mais_velha(lista)
    idadeMaisNova = pessoa_mais_nova(lista)
    
    dIdade = doenca_por_intervalo_idade(lista,idadeMaisNova,idadeMaisVelha,10)
    #print_doenca_intervalo_idade(dIdade)
    #print_doenca_intervalo_idade(doenca_por_intervaloDefault_idade(lista,idadeMaisNova,idadeMaisVelha))
    
    colesterol_mais_alto=nivel_mais_alto(lista)
    colesterol_mais_baixo = nivel_mais_baixo(lista)
    
    dColesterol = doenca_por_intervalo_colesterol(lista,colesterol_mais_baixo,colesterol_mais_alto)
    #print_colesterol(dColesterol,len(lista))

    tabular(dSexo,1)
    tabular(dIdade,2)
    tabular(dColesterol,3)
    
    
if __name__ == "__main__":
    main()
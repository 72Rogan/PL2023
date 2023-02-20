import sys
from tabulate import tabulate
import matplotlib.pyplot as plt
import os


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
 
 
#----------------------------------- Utils ----------------------------------------- 
def divide (a,b):
    if b ==0:
        return 0
    else:
        return a/b
        
def incremento(dicGeral,dicEsp,valor):
    for key in dicEsp.keys():
        limiteInf,limiteSup = key.split("-")
        if(valor>=int(limiteInf) and valor<=int(limiteSup)):
            dicEsp[key]["Total"] +=1
            if(dicGeral["temDoenca"]==1):
                dicEsp[key]["Doentes"] +=1
                
def calcula_Percentagem(dic):
        for key in dic.keys():
            aux = divide(dic[key]["Doentes"],dic[key]["Total"])*100
            dic[key]["Percentagem"] = str(aux) + "%"

def inicializacao(dic,limite_sup,limite_inf, max, intervalo):
    while(limite_sup<max):
        limite_sup = limite_inf + intervalo
        dic[f"{limite_inf}-{limite_sup}"] = {"Doentes":0,"Total":0,"Percentagem":0};
        limite_inf = limite_sup + 1

def prettyPrint(dict):
    print("\n")
    for key in dict.keys():
        doentes = dict[key]["Doentes"]
        total = dict[key]["Total"]
        perc = dict[key]["Percentagem"]
        print(f"Intervalo:{key} --> {doentes} doentes em {total} pessoas ---> {perc}%") 
    print("\n")

#--------------------------------- Exercício 1 -------------------------------------
#função que recebe uma lista de dicionarios e devolve um dicionario com duas chaves 
#("M", "F") em que cada valor corresponde ao número de doentes desse sexo

def doencas_por_sexo(lista):
    dict_doencas_por_sexo = {'M':{"Doentes":0,"Total":0,"Percentagem":0},'F':{"Doentes":0,"Total":0,"Percentagem":0}}
    
    for dict in lista:
        if(dict['sexo'].upper() == "M"):
            dict_doencas_por_sexo["M"]["Total"]+=1
            if(dict["temDoenca"]==1):
                dict_doencas_por_sexo["M"]["Doentes"]+=1
        elif(dict["sexo"].upper()=='F'):
            dict_doencas_por_sexo["F"]["Total"]+=1
            if(dict["temDoenca"]==1):
                dict_doencas_por_sexo["F"]["Doentes"]+=1
                
    calcula_Percentagem(dict_doencas_por_sexo)
    return dict_doencas_por_sexo
    
def print_sexo(dict):
    homens_doentes = dict["M"]["Doentes"]
    homens_total = dict["M"]["Total"]
    mulheres_doentes = dict["F"]["Doentes"]
    mulheres_total = dict["F"]["Total"]  
    homens_percentagem = dict["M"]["Percentagem"]
    mulheres_percentagem = dict["F"]["Percentagem"]
    
    print(f"\n{homens_doentes} homens doentes em {homens_total} homens ---> {homens_percentagem}%")
    print(f"{mulheres_doentes} mulheres doentes em {mulheres_total} mulheres ---> {mulheres_percentagem}%\n")
    

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
    inicializacao(dicionario_intervalo_idade,limite_sup,limite_inf,maior_idade,intervalo)
    for dic in lista:
        idade = int(dic["idade"])
        incremento(dic,dicionario_intervalo_idade,idade)
    calcula_Percentagem(dicionario_intervalo_idade)
    return dicionario_intervalo_idade
        
def doenca_por_intervaloDefault_idade(lista,menor_idade,maior_idade):
    intervalo = 5
    dicionario_intervalo_idade = dict()
    limite_inf = menor_idade 
    limite_sup =0
    
    while(limite_sup<maior_idade):
        limite_sup = limite_inf + intervalo
        dicionario_intervalo_idade[f"{limite_inf}-{limite_sup}"] = {"Doentes":0,"Total":0,"Percentagem":0};
        limite_inf = limite_sup + 1
   
    for dic in lista:
        idade = int(dic["idade"])
        for key in dicionario_intervalo_idade.keys():
                menor,maior = key.split("-")
                if(idade>=int(menor) and idade<=int(maior)):
                    dicionario_intervalo_idade[key]["Total"] +=1
                    if(dic["temDoenca"]==1):
                        dicionario_intervalo_idade[key]["Doentes"] +=1
    
    for key in dicionario_intervalo_idade.keys():
        aux = (dicionario_intervalo_idade[key]["Doentes"]/dicionario_intervalo_idade[key]["Total"])*100
        dicionario_intervalo_idade[key]["Percentagem"] = str(aux) + "%"
   
    return dicionario_intervalo_idade

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

def nivel_mais_baixo(lista):
    menor_nivel = lista[0]["colesterol"]
    for dict in lista:
        if(dict["colesterol"]<=menor_nivel):
            menor_nivel=dict["colesterol"]
    return int(menor_nivel)

def doenca_por_intervalo_colesterol(lista,menor_nivel,maior_nivel):
    intervalo = 9
    dicionario_intervalo_colesterol = dict()
    limite_inf = menor_nivel
    limite_sup=0
    
    inicializacao(dicionario_intervalo_colesterol,limite_sup,limite_inf,maior_nivel,intervalo)
        
    for dic in lista:
        nivel = int(dic["colesterol"])
        incremento(dic,dicionario_intervalo_colesterol,nivel)
                    
    calcula_Percentagem(dicionario_intervalo_colesterol)                             
                    
    return dicionario_intervalo_colesterol   

#---------------------------------- Exercício 4 ------------------------------------
def tabular(dic,escolha):
    #1 - sexo : 2 - idade : 3 - colesterol
    table = []
    if(escolha==1):
        headers = ['Sexo', 'Quantidade Doente',"Quantidade Total", "Percentagem"]  
    if(escolha==2):
        headers = ['Intervalo idade', 'Quantidade Doente',"Quantidade Total","Percentagem"]
    if(escolha==3):
        headers = ['Intervalo colesterol', 'Quantidade Doente',"Quantidade Total","Percentagem"]

    for (chave, valores) in dic.items():
            doentes = valores["Doentes"]
            total = valores["Total"]
            percentagem = valores["Percentagem"]
            table.append([chave, doentes, total, percentagem])
            
    print(tabulate(table, headers=headers))
    print("\n")

##---------------------------------- Exercício Extra ------------------------------------
def grafo(dict,escolha):
    
    # extract the categories and values
    chaves = list(dict.keys())
    values_doentes = [dict[key]["Doentes"] for key in chaves]
    values_total = [dict[cat]["Total"] for cat in chaves]
    
    # create a bar chart
    fig, ax = plt.subplots()
    ax.bar(chaves, values_doentes, label='Doentes')
    ax.bar(chaves, values_total, bottom=values_doentes, label='Total')
    ax.legend()
    
    if(escolha==1):
        plt.xlabel('Sexo')
        plt.ylabel('Quantidade')
        plt.title('Quantidade de doentes por Sexo')
    if(escolha==2):
        plt.xlabel('Idade')
        plt.ylabel('Quantidade')
        plt.title('Quantidade de doentes por Idade')
    if(escolha==3):
        #plt.bar(dict.keys(), dict.values())
        plt.xlabel('Colesterol')
        plt.ylabel('Quantidade')
        plt.title('Quantidade de doentes por Colesterol')
    
    # Display the plot
    plt.show()
 
 
#------------------------------------------ Interface -------------------------------
def mainMenu():
    os.system("clear")
    print("┌────────────────────────────────────────────────────────────────┐")
    print("│                            MAIN MENU                           │")
    print("├────────────────────────────────────────────────────────────────┤")
    print("│                      1 ─ Distribuição por Sexo                 │")
    print("│                      2 ─ Distribuição por Idade                │")
    print("│                      3 ─ Distribuição por Colesterol           │")
    print("│                      0 ─ SAIR                                  │")
    print("└────────────────────────────────────────────────────────────────┘")
   
def entrada():
 return int(input("ENTRADA ──> "))
    
def entradaInvalida():
    os.system("clear")
    print("┌────────────────────────────────────────────────────────────────┐")
    print("│                        ENTRADA INVÁLIDA                        │")
    print("└────────────────────────────────────────────────────────────────┘")


def sair():
    os.system("clear")
    print("┌────────────────────────────────────────────────────────────────┐")
    print("│                             A SAIR...                          │")
    print("└────────────────────────────────────────────────────────────────┘")

def main():
    dir = "../TPC1/myheart.csv"
    lista = parse_file(sys.argv[1])
    
    flag=True
    while(flag):
        mainMenu()
        mainMenuVar = entrada()
        
        if mainMenuVar == 0:
            sair()
            flag = False
        
        elif mainMenuVar == 1:
            dSexo = doencas_por_sexo(lista)
            print_sexo(dSexo)
            tabular(dSexo,1)
            grafo(dSexo,1)
        elif mainMenuVar == 2:
                idadeMaisVelha = pessoa_mais_velha(lista)
                idadeMaisNova = pessoa_mais_nova(lista)
                print(f"\nPessoa mais nova com idade de {idadeMaisNova}")
                print(f"Pessoa mais velha com idade de {idadeMaisVelha}\n")
                
                dIdade = doenca_por_intervalo_idade(lista,idadeMaisNova,idadeMaisVelha,10)
                prettyPrint(dIdade)
                tabular(dIdade,2)
                grafo(dIdade,2)
                
        elif mainMenuVar == 3:
            colesterol_mais_alto=nivel_mais_alto(lista)
            colesterol_mais_baixo = nivel_mais_baixo(lista)
            print(f"\nNível de colesterol mais alto: {colesterol_mais_alto}")
            print(f"Nível de colesterol mais baixo: {colesterol_mais_baixo}\n")
            dColesterol = doenca_por_intervalo_colesterol(lista,colesterol_mais_baixo,colesterol_mais_alto)
            prettyPrint(dColesterol)
            tabular(dColesterol,3)
            grafo(dColesterol,3)
        else:
            entradaInvalida()
    
if __name__ == "__main__":
    main()
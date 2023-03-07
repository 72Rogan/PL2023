import re
import json
from prettytable import PrettyTable

#Função de Parseing do ficheiro 
def open_File(diretoria):
    final_data = []
    with open(diretoria,"r") as file:
        content = file.readlines()
        pattern = re.compile(r'^(?P<proc>\d+)::(?P<data_Ano>\d{4})\-(?P<data_Mes>\d{2})\-(?P<data_Dia>\d{2})::(?P<nome>(\w+\s*)+)::(?P<pai>(\w+\s*)+)::(?P<mae>(\w+\s*)+)::(?P<obs>(.*))::')
        for linha in content:
            result = pattern.match(linha)
            if result != None:
                final_data.append(result.groupdict())
    return final_data

#Alínea A
def freq_por_ano(data):
    anos = dict()
    
    for i in range(len(data)):
        ano = data[i]["data_Ano"]
        
        if ano not in anos:
            anos[ano] = 1
        else:
            anos[ano] +=1      
    return anos
 
#Alínea B
def sec(data):
    nome_proprio = {}
    nome_apelido = {}

    for entrada in data:
        
        sec = int(entrada["data_Ano"]) // 100 + 1
        nome = re.match(r"(\w+)\b",entrada["nome"]).group(1)
        apelido = re.search(r"\b(\w+)$",entrada["nome"]).group()
        
        if sec not in nome_proprio:
            nome_proprio[sec] = {}
        if sec not in nome_apelido:
            nome_apelido[sec] = {}
        
        if nome not in nome_proprio[sec]:
            nome_proprio[sec][nome] = 1
        else:
            nome_proprio[sec][nome] +=1
            
        if apelido not in nome_apelido[sec]:
            nome_apelido[sec][apelido] = 1
        else:
            nome_apelido[sec][apelido] +=1   
     
    top_nomeP = (sorted(nome_proprio.items(), reverse=True))
    top_nomeA = (sorted(nome_apelido.items(), reverse=True))
    
    return top_nomeP,top_nomeA

#Alínea C
def relacao(data):
    familia = dict()
    parente = re.compile(r'[a-zA-Z ]*,([A-Za-z ]*)\.[ ]*Proc\.[0-9]+\.')
    
    for entrada in data:
        obs = entrada["obs"]
        resultados = parente.findall(obs)
        
        for r in resultados:
            if r not in familia:
                familia[r] = 1
            else:
                familia[r] += 1
    return familia

#Alínea D
def outJ(data,file_path):
    with open(file_path, "w+") as f:
        json.dump(data[:20], f)

def prettyprint(dict, alinea):
    table = PrettyTable()
    if alinea == "A":
        table.field_names = ["Ano","Num"]
        for key, value in dict.items():
            table.add_row([key, value])
    elif alinea == "B":
        table.field_names = ["Sec","Nome","Num"]
        
        for sec, d in dict:
            for (nome, num) in d.items():
                table.add_row([sec, nome, num])

    elif alinea == "C":
        table.field_names = ["Parente","Num"]
        for key, value in dict.items():
            table.add_row([key, value])
    print(table) 
       
def main():
    data = open_File('/home/rogan/Desktop/3ano2sem/pl/PL2023/TPC3/entrada/teste.txt')
    flag = True
    while flag :
        print("\n+----------------------------------------------------------------------------------+")
        print("|                                 Selecione uma opção                              |")
        print("+----------------------------------------------------------------------------------+")
        print("| 1 Frequência de processos por ano                                                |")
        print("| 2 Frequência de nomes próprios e apelidos por séculos                            |")
        print("| 3 Frequência dos vários tipos de relação                                         |")
        print("| 4 Converter os 20 primeiros registos num novo ficheiro de output em formato Json |")
        print("| 0 Sair                                                                           |")
        print("+----------------------------------------------------------------------------------+")
        opcao = input("Opção escolhida: ")
    
        if opcao == "1":
            # Frequência de processos por ano
            alineaA= freq_por_ano(data)
            prettyprint(alineaA,"A")
            
        elif opcao == "2":
            #Frequência de nomes próprios nos séculos
            alineaBN,alineaBA = sec(data)
            prettyprint(alineaBN,"B")
            prettyprint(alineaBA,"B")
        elif opcao == "3":
            #Frequência dos vários tipos de relação
            alineaC = relacao(data)
            prettyprint(alineaC,"C")
            
        elif opcao == "4":
            # Faz a conversão para ficheiro json
            outJ(data,'/home/rogan/Desktop/3ano2sem/pl/PL2023/TPC3/saida/out.json')
            
        elif opcao == "0":
            flag = False
            break
        else:
            print("Opção inválida. Tente novamente.")
        
if __name__ == '__main__':
    main()
    
import os
import re

def leTerminal():
    input_str = input("Coloque o texto...\n")
    
    return input_str
    
def parseLinha(linha):
    somatorio = 0
    num = ' '
    flag_ON=True
    
    for i in range(len(linha)):
        if (re.match(r'[0-9]', linha[i]) and flag_ON):
            if(linha[i+1] ==' ' or not(re.match(r'[0-9]', linha[i+1]))):
                somatorio += int(linha[i])
            else:
                e = i
                while (linha[e]!=' ' and (re.match(r'[0-9]', linha[i+1]))):
                    num += (linha[e])
                    e+=1
                i+=e
                somatorio += int(num)
            
        elif (linha[i].upper()=='O' and linha[i+1].upper()=='F' and linha[i+2].upper()=='F'):
            i+=2
            flag_ON = False
        elif (linha[i].upper()=='O' and linha[i+1].upper()=='N'):
            i+=2
            flag_ON = True
        elif(linha[i]=="="):
            break
    return somatorio

def main():
   print(parseLinha(leTerminal()))
   
   

if __name__ == '__main__':
    main()
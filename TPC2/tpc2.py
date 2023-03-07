import os
import re

def leTerminal():
    input_str = input("Coloque o texto...\n")
    
    return input_str
    
def parseLinha(linha):
    somatorio = 0
    num = ''
    flag_ON=True
    i=0
    while i in range(len(linha)):
        if (re.match(r'[0-9]', linha[i]) and flag_ON):
            if(linha[i+1] ==' ' or not(re.match(r'[0-9]', linha[i+1]))):
                somatorio += int(linha[i])
                i+=1
            else:
                e = i
                while (linha[e+1]!=' ' and re.match(r'[0-9]', linha[e+1])) :
                    num += (linha[e])
                    #num+=linha[e+1]
                    e+=1
                if re.match(r'[0-9]', linha[e]):
                    num += (linha[e])
                    #num+=linha[e+1]
                    e+=1
                somatorio += int(num)
                num = ''
                i=e
           
        elif (linha[i].upper()=='O' and linha[i+1].upper()=='F' and linha[i+2].upper()=='F'):
            i+=3
            flag_ON = False
        elif (linha[i].upper()=='O' and linha[i+1].upper()=='N'):
            i+=2
            flag_ON = True
        elif(linha[i]=="=" and flag_ON):
            break
        else:
            i+=1
    return somatorio

def main():
   #print(parseLinha("12 a1a on 123a off 1 ="))

   print(parseLinha(leTerminal()))
   

if __name__ == '__main__':
    main()
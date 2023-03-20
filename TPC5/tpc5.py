import ply.lex as lex
import re

saldo = 0
tel = 0 #estado dele -» 0:pousado; 1:levantado; 2:abortar

# List of token names.   This is always required
tokens = (
   'LEVANTAR',
   'POUSAR',
   'MOEDA',
   'NUMERO',
   'ABORTAR',
)

# Regular expression rules for simple tokens

t_LEVANTAR = r"LEVANTAR"
t_POUSAR = r"POUSAR"
t_ABORTAR = r"ABORTAR"

# A regular expression rule with some action code
def t_MOEDA(t):
    r"MOEDA\s((\w+\,?\s?)+)."
    match = re.match(r"MOEDA\s((\w+\,?\s?)+)", t.value)
    t.value = match.group(1)
    return t

def t_NUMERO(t):
    r'T=(\d+)'
    m = re.match(r'T=(\d+)',t.value)
    t.value = m.group(1)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
#t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def calcula_Saldo(saldo):
    euro = int(saldo/100)
    centimos = saldo - 100*euro
    return (f"{euro}e{centimos}c")


def parse_Moeda(lista):
    global saldo
    euros = re.findall(r"(\d)e",lista)
    cent = re.findall(r"(\d+)c",lista)
    s=""
    for numero in cent:
        if (int(numero) != 1 and int(numero) != 2 and int(numero) != 5 and int(numero) != 10 and int(numero) != 20 and int(numero) != 50):
            s += f"maq: \"{str(numero)}c - moeda inválida;" 
        else: 
            saldo += int(numero)

    for numero in euros:
        if (int(numero) != 1 and int(numero) != 2):
            s += f"maq: \"{str(numero)}e - moeda inválida;" 
        else: 
            saldo += int(numero)*100

    s += " saldo = " + calcula_Saldo(saldo) +"\""

    return s

def parse_Numero(num):
    global saldo
    if(num[:3]=="601"or num[:3]=="641"):
        print("maq: \"Esse número não é permitido neste telefone. Queira discar novo número!\"")
    elif(num[:2]=="00"):
        if(saldo<150):
            print("maq: \"Saldo Insuficiente\"")
        elif(saldo>=150):
            saldo-=150
            print("maq: \"saldo = "+calcula_Saldo(saldo)+"\"")
    elif(num[:1]=="2"):
        if(saldo<25):
            print("maq: Saldo Insuficiente")
        elif(saldo>=25):
            saldo-=25
            print("maq: \"saldo = "+calcula_Saldo(saldo)+"\"")
    elif(num[:3]=="800"):    
        print("maq: \"saldo = "+saldo+"\"")
    elif(num[:3]=="808"):
        if(saldo<10):
            print("maq: Saldo Insuficiente")
        elif(saldo>=10):
            saldo-=10
            print("maq: \"saldo = "+calcula_Saldo(saldo)+"\"")
 
def troco(bolsa):
    troco={"2e":0,"1e":0,"50c":0,"20c":0,"10c":0,"5c":0,"2c":0,"1c":0}
    
    euro = int(bolsa/100)
    centimos = bolsa - 100*euro
    
    if(euro%2==0):
        troco["2e"]=int(euro/2)
    elif(euro%2!=0):
        troco["2e"]=int(euro/2)
        troco["1e"]=int(euro%2)
        
    if(centimos%50==0):
        troco["50c"]=int(centimos/50)
    elif(centimos%50!=0):
        troco["50c"]=int(centimos/50)
        centimos -= 50*int(centimos/50)
        if(centimos%20==0):
            troco["20c"]=int(centimos/20)
        elif(centimos%20!=0):
            troco["20c"]=int(centimos/20)
            centimos-=20*int(centimos/20)
            if(centimos%10==0):
                troco["10c"]=int(centimos/10)
            elif(centimos%10!=0):
                troco["10c"]=int(centimos/10)
                centimos-=10*int(centimos/10)
                if(centimos%5==0):
                    troco["5c"]=int(centimos/5)
                elif(centimos%5!=0):
                    troco["5c"]=int(centimos/5)
                    centimos-=5*int(centimos/5)
                    if(centimos%2==0):
                        troco["2c"]=int(centimos/2)
                    elif(centimos%5!=0):
                        troco["2c"]=int(centimos/2)
                        centimos-=2*int(centimos/2)
                        if(centimos%1==0):
                            troco["1c"]==int(centimos/1)
    
    dictString=""
    for key,value in troco.items():
        dictString+=f"{value}x{key}, "
    
    mystring = "maq: \"troco="+calcula_Saldo(saldo)+"; Volte sempre!\" ou maq: \"troco="+dictString[:-2]+"; Volte sempre!\""
    
    return mystring
    
    
def parse_token(t):
    global tel
    if(t.type=="LEVANTAR"):
        if(tel==1):
            print("maq: O telefone já se encontra Levantado...")
        if(tel==0):
            print("maq: Introduza moedas.")
            tel=1
            
    if(t.type=="MOEDA"):
        if(tel==0):
            print("maq: O telefone já se encontra Pousado...")
        else:
            print(parse_Moeda(t.value))
        
    if(t.type=="NUMERO"):
        if(tel==0):
            print("maq: O telefone já se encontra Pousado...")
        else:
            parse_Numero(t.value) 
        
    if(t.type=="POUSAR"):
        if(tel==0):
            print("maq: O telefone já se encontra Pousado...")
            tel=0
        if(tel==1):
            print(troco(saldo))
    if(t.type=="ABORTAR"):
        if(tel==0):
            print("maq: O telefone já se encontra Pousado...")
        else:
            tel=2
                
        
        
def main():
    global tel
    lexer = lex.lex()
    while(True):
        info = input("> ")
        lexer.input(info)
        for token in lexer:
            parse_token(token)
        if (tel == 2): break

if __name__ == "__main__":
    main()
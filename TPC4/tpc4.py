import re
import sys
import json

def lista(notas):
    matches = re.findall(r"\d+",notas)
    return [int(m) for m in matches]
    
def do_op(notas,op):
    if op == "sum":
        return sum(notas)
            
    elif op == "media":
        return sum(notas)/len(notas)

    
def parse2Json(dir_source,dir_dest):

    with open(dir_source, 'r') as f:
        
        linhas = [s.strip() for s in f.readlines()]
       
    #lista com as info do header
    header = re.findall(r"(\w+(?:\{\d+(?:,\d+)?\}(?:::\w+)?)?)",linhas[0])
    
    #Reorganiza o header e coloca nos dicts casos extra
    intervalo = {}
    operacao = {}
    for i in range(0, len(header)):
        if match := re.search(r"(\w+)\{(\d+)(?:,(\d+))?\}(?:::(\w+))?", header[i]):
            header[i] = match.group(1)

            if match.group(3) is None:
                intervalo[header[i]] = (int(match.group(2)), None)
            else:
                intervalo[header[i]] = (int(match.group(2)), int(match.group(3)))

            if match.group(4) is not None:
                operacao[header[i]] = match.group(4)
    
    #ciclo para criar o pattern para o ficheiro
    pattern = ""
    for item in header:
        numNotas=""
        if item in intervalo:
            if intervalo[item][1] == None:
                numNotas=f"{{ {intervalo[item][0]} }}"
            else:
                numNotas=f"{{{intervalo[item][0]},{intervalo[item][1]}}}"
            
            pattern += f"(?P<{item}>([^,;]+[,;]?){numNotas})"
        else:
            pattern += rf"(?P<{item}>[^,;]+)[,;]"
    
    info = []
    for line in linhas[1:]:
        correspondencia = re.finditer(pattern,line)
        
        for c in correspondencia:
            info += [c.groupdict()]
      
    for i in range(0, len(info)):
        for k in info[i]:
            if k in intervalo:
                info[i][k] = lista(info[i][k])
            if k in operacao:
                info[i][k] = do_op(info[i][k],operacao[k])
              
              
              
    with open(dir_dest, "w+") as f:
        json.dump(info, f, indent=4, ensure_ascii=False)

def main():
    source = sys.argv[1]
    destiny = sys.argv[2]
    parse2Json(source,destiny)
    
if __name__ == '__main__':
    main()

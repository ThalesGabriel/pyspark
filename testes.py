import csv

arquivo = open("csv/A370.csv")
linhas = csv.reader(arquivo)
data = ['']*4

for linha in linhas:
    if linha[0]=="timestamp":
        continue
    time=linha[0]
    data[0]=linha[8]
    data[1]=linha[9]
    data[2]=linha[10]
    data[3]=linha[16]
    print(time, data)

""" 
for f in listdir("csv/"):
    arquivo = open(f)
    linhas = csv.reader(arquivo)
    for j in linhas:
        time = linhas
        data = """

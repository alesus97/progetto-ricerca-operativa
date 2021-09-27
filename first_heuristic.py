import time

File = open("input.txt","r") #lettura file
Lines = File.readlines()
File.close()

Split_Line = Lines[0].split(" ") #suddivido per campi la prima riga del file di input
Num_pianeti = int(Split_Line[0])
Litri_carburante = int(Split_Line[1])
Num_contenitori = int(Split_Line[2])
Tipi_liquido = int(Split_Line[2])

Split_Line = Lines[1].split(" ") #suddivido per campi la seconda riga del file di input
Capacita1 = int(Split_Line[0])
Capacita2 = int(Split_Line[1])
Capacita3 = int(Split_Line[2])
Capacita4 = int(Split_Line[3])
Capacita5 = int(Split_Line[4])

#creazione dizionario (per ogni riga ho la quantità di liquidi per pianeta, la chiave è l'id del pianeta)
Quantita_liquido = {}

Id_pianeta = 2
for k in range(Num_pianeti) :
    Split_Line = Lines[Id_pianeta].split(" ")
    Quantita_liquido[k] = (int (Split_Line[1]),int (Split_Line[2]),int (Split_Line[3]),int (Split_Line[4]),int (Split_Line[5]))
    Id_pianeta = Id_pianeta + 1
    
Pianeti_raggiungibili = {}
start = 20002
posizione = 0 #pianeta di partenza

for k in range(start,len(Lines),1) : 
    Split_Line = Lines[start].split(" ")
    Pianeti_raggiungibili[k] = (int (Split_Line[0]),int (Split_Line[1]),int (Split_Line[2]))
    start = start + 1

indice = []      # pianeta raggiungibile dal pianeta corrente
carburante = []  
carburante_rimanente = Litri_carburante
contenitori = [0,0,0,0,0]
minimo = 0
capacita_residua = [Capacita1,Capacita2,Capacita3,Capacita4,Capacita5]
pianeti_visitati = [0]
stop = False

#Euristica greedy

t = time.time()
while(carburante_rimanente > 0 and not stop):
    indice = []
    carburante = []
   # print("Pianeta corrente:",posizione,"\n")
   # print("Carburante rimanente:",carburante_rimanente,"\n")
    for j in Pianeti_raggiungibili:
        if posizione == Pianeti_raggiungibili[j][0] and Pianeti_raggiungibili[j][1] not in pianeti_visitati:
            indice.append(Pianeti_raggiungibili[j][1]) 
            carburante.append(Pianeti_raggiungibili[j][2])
            

    if(len(indice) > 0): 
        minimo = min(carburante)
       # print("Pianeti raggiungibili dal pianeta corrente:",indice,"\n")
       # print("Carburante necessario a raggiungere i pianeti:",carburante,"\n")
       # print("Percorso minimo:",minimo,"\n")
        for i in range(len(carburante)) :
            if minimo == carburante[i]:
                if carburante_rimanente >= carburante[i]:
                    posizione = indice[i]
                    pianeti_visitati.append(posizione)
                    carburante_rimanente = carburante_rimanente - carburante[i]
                    for k in range(Tipi_liquido):
                        if capacita_residua[k] >= Quantita_liquido[posizione][k]:
                            capacita_residua[k] = capacita_residua[k] - Quantita_liquido[posizione][k]
                            contenitori[k] = contenitori[k] + Quantita_liquido[posizione][k] 
                break
    else:
        stop = True
        
        punteggio = 0.4*(len(pianeti_visitati)) + 0.6*sum(contenitori)

elapsed = time.time() - t
print("Tempo di elaborazione:" + str(elapsed))
print("Carburante rimamente:" + str(carburante_rimanente))
print("Liquido di tipo 1 raccolto:" + str(contenitori[0]))
print("Liquido di tipo 2 raccolto:" + str(contenitori[1]))
print("Liquido di tipo 3 raccolto:" + str(contenitori[2]))
print("Liquido di tipo 4 raccolto:" + str(contenitori[3]))
print("Liquido di tipo 5 raccolto:" + str(contenitori[4]))
print("Numero di pianeti raggiunti:" + str(len(pianeti_visitati)))
print("score finale: " + str(punteggio))

# f = open("output.txt","w")

# value = ("Pianeti raggiunti:", len(pianeti_visitati))
# value1 = ("Carburante rimanente:",carburante_rimanente)
# value2 = ("Punteggio",punteggio)
# value3 = ("Pianeti visitati", pianeti_visitati)

# s = str(value) + "\n" # converte la tupla in una stringa
# s1 = str(value1) + "\n" 
# s2 = str(value2) + "\n"
# s3 = str(value3) + "\n"

# f.writelines(s)
# f.writelines(s1)
# f.writelines(s2)
# f.writelines(s3)


# f.close()
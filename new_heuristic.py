import time

File = open("input.txt","r") # lettura file
Lines = File.readlines()
File.close()

# Prima riga
Split_Line = Lines[0].split(" ") #suddivido per campi la prima riga del file di input
Num_pianeti = int(Split_Line[0])
total_fuel = int(Split_Line[1])
Num_contenitori = int(Split_Line[2])
Tipi_liquido = int(Split_Line[2])

# 2a riga
Split_Line = Lines[1].split(" ") #suddivido per campi la seconda riga del file di input
Capacita1 = int(Split_Line[0])
Capacita2 = int(Split_Line[1])
Capacita3 = int(Split_Line[2])
Capacita4 = int(Split_Line[3])
Capacita5 = int(Split_Line[4])

section_1 = Lines[2:20002]

liquid_for_planets = []

for line in section_1:
    current_line = line.split(' ')
    new_elem = {}
    new_elem['id'] = current_line[0]
    new_elem['liquid1'] = current_line[1]
    new_elem['liquid2'] = current_line[2]
    new_elem['liquid3'] = current_line[3]
    new_elem['liquid4'] = current_line[4]
    new_elem['liquid5'] = current_line[5][:-1]
    new_elem['taken'] = False
    liquid_for_planets.append(new_elem)
    
section_2 = Lines[20002:]

edges = []
edge_counter = 0
for line in section_2:
    current_line = line.split(' ')
    new_elem = {}
    new_elem['planet_A'] = current_line[0]
    new_elem['planet_B'] = current_line[1]
    new_elem['cost'] = current_line[2][:-1]
    new_elem['id'] = edge_counter
    edges.append(new_elem)
    edge_counter += 1
    
# Costo totale
total_cost = 0
unique_planets = 0
total_liquid_amount = 0
remaining_fuel = total_fuel

# indice dell'iterazione precedente
last_edge_index = 0
taken_liquid = [0,0,0,0,0]

current_node_id = 0 

t = time.time()

while remaining_fuel > 0: 
    
    # Archi percorribili
    current_edges = []
    
    # Recupero archi percorribili
    while last_edge_index < len(edges) and int(edges[last_edge_index]['planet_A']) == current_node_id:
        current_edges.append(edges[last_edge_index])
        last_edge_index += 1

    if len(current_edges) == 0:
        break

    # Recupero info su chi e' stato visitato 
    for possible_route in current_edges:
        possible_id = int(possible_route['planet_B'])

        possible_route['taken'] = liquid_for_planets[possible_id]['taken']

    # Scelta in base a costo minore tra i non visitati oppure costo minore se tutti visitati

    # Costruzione lista di tuple costo,taken
    cost_list = []
    for possible_choice in current_edges:
        cost_list.append((int(possible_choice['cost']), possible_choice['taken']))
        
    # Lista temporanea senza i nodi visitati
    temp_cost_list = cost_list
    for cost in cost_list:
        if cost[1]: # Se c'e' un True lo rimuove
            temp_cost_list.remove(cost)

       
    # Se la lista temponanea e' vuota scegli a costo minore dalla lista originaria
    if (len(temp_cost_list) == 0):
        min_cost = min(cost_list)
        chosen_edge = current_edges[cost_list.index((min_cost[0], min_cost[1]))] # arco scelto

        # Recupero posizione dell'arco scelto nella lista
        for edge in edges:
            if chosen_edge['planet_B'] == edge['planet_A']:
                last_edge_index = edge['id']
                break

        # Aggiorno carburante
        if remaining_fuel - int(chosen_edge['cost']) > 0:
            remaining_fuel = remaining_fuel - int(chosen_edge['cost'])
        else: 
            break
        
    # Altrimenti scegli tra i nodi non vistati
    else:
        min_cost = min(temp_cost_list)
        chosen_edge = current_edges[temp_cost_list.index((min_cost[0], min_cost[1]))]

        # Recupero posizione dell'arco scelto nella lista
        for edge in edges:
            if chosen_edge['planet_B'] == edge['planet_A']:
                last_edge_index = edge['id']
                break

        # Aggiorno carburante
        if remaining_fuel - int(chosen_edge['cost']) > 0:
            remaining_fuel = remaining_fuel - int(chosen_edge['cost'])
        else: 
            break
            
        # Aggiorno liquidi raccolti
        if taken_liquid[0] + int(liquid_for_planets[int(chosen_edge['planet_B'])]['liquid1']) < Capacita1: taken_liquid[0] += int(liquid_for_planets[int(chosen_edge['planet_B'])]['liquid1'])
        if taken_liquid[1] + int(liquid_for_planets[int(chosen_edge['planet_B'])]['liquid2']) < Capacita2: taken_liquid[1] += int(liquid_for_planets[int(chosen_edge['planet_B'])]['liquid2'])
        if taken_liquid[2] + int(liquid_for_planets[int(chosen_edge['planet_B'])]['liquid3']) < Capacita3: taken_liquid[2] += int(liquid_for_planets[int(chosen_edge['planet_B'])]['liquid3'])
        if taken_liquid[3] + int(liquid_for_planets[int(chosen_edge['planet_B'])]['liquid4']) < Capacita4: taken_liquid[3] += int(liquid_for_planets[int(chosen_edge['planet_B'])]['liquid4'])
        if taken_liquid[4] + int(liquid_for_planets[int(chosen_edge['planet_B'])]['liquid5']) < Capacita5: taken_liquid[4] += int(liquid_for_planets[int(chosen_edge['planet_B'])]['liquid5'])

        # Settaggio taken sul nodo scelto
        for elem in liquid_for_planets:
            if elem['id'] == chosen_edge['planet_B']:
                elem['taken'] = True
                unique_planets += 1
                break

    current_node_id = int(chosen_edge['planet_B']) # aggiorna nodo corrente

    score = 0.6 * unique_planets + 0.6 * sum(taken_liquid)
    #print(score)

elapsed = time.time() - t
print("Tempo di elaborazione:" + str(elapsed))
print("Carburante rimamente:" + str(remaining_fuel))
print("Liquido di tipo 1 raccolto:" + str(taken_liquid[0]))
print("Liquido di tipo 2 raccolto:" + str(taken_liquid[1]))
print("Liquido di tipo 3 raccolto:" + str(taken_liquid[2]))
print("Liquido di tipo 4 raccolto:" + str(taken_liquid[3]))
print("Liquido di tipo 5 raccolto:" + str(taken_liquid[4]))
print("Numero di pianeti raggiunti:" + str(unique_planets))
print("score finale: " + str(score))

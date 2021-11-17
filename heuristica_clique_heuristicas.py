# Funcion de parseo:

def parsear_archivo(nombre_archivo):
    with open(nombre_archivo) as file:  
        data = [line.split() for line in file.readlines()]
    incompatibilidades = []
    tiempos_prendas = dict()
    for i in range(len(data)):
        if (data[i][0] == 'e'):
            incompatibilidades.append(data[i][1:])
        elif (data[i][0] == 'n'):
            tiempos_prendas[int(data[i][1])] = int(data[i][2])
    sorted(tiempos_prendas.items(), key=lambda x: x[1])
    return incompatibilidades, tiempos_prendas

# Funciones de matrices:

def matriz_de_incompatibilidades(incompatibilidades):
    res = dict()
    for s1, s2 in incompatibilidades:
        n1, n2 = int(s1), int(s2)
        if(n1 in res.keys()):
            res[n1].add(n2)
        else:
            res[n1] = {n2}
        if(n2 in res.keys()):
            res[n2].add(n1)
        else:
            res[n2] = {n1}    
    return res

def matriz_de_compatibilidades(incompatibilidades):
    res = matriz_de_incompatibilidades(incompatibilidades)
    nodos = set(res.keys())
    for n in nodos:
        res[n] = nodos.difference(res[n].union({n}))
    return res

def dropVetex(M, vertex):
    M2 = M.copy()
    del M2[vertex]
    for x in M2.keys():
        M2[x]= [w for w in M2[x] if w!=vertex]
    return M2

def drop_vertices(M, verices):
    M2 = M.copy()
    for v in verices:
        M2 = dropVetex(M2, v)
    return M2

# Funciones de clique:

def find_single_clique(graph, start_vertex):
    clique = []
    vertices = list(graph.keys())
    clique.append(vertices[start_vertex])
    for v in vertices:
        if v in clique:
            continue
        isNext = True
        for u in clique:
            if u in graph[v]:
                continue
            else:
                isNext = False
                break
        if isNext:
            clique.append(v)
    return sorted(clique)

def finds_cliques(M):
    cliques = set()
    for vertex in range(0, len(M.keys())):
        cliques.add(tuple(find_single_clique(M, vertex)))
    return list(cliques)


# Heuristicas

def heuristica_clique_mas_ahorro(M, datos_prendas):
    cliques = finds_cliques(M)
    valores_maximos = []
    for clique in cliques:
        valores = []
        for x in clique:
            valores.append(datos_prendas[x])
        valores_maximos.append(sum(valores) - max(valores))
    index_max = valores_maximos.index(max(valores_maximos))
    return cliques[index_max]

def heuristica_clique_mas_largo(M, datos_prendas):
    cliques = finds_cliques(M)
    lengths = []
    for clique in cliques:
        lengths.append(len(clique))
    index_largest = lengths.index(max(lengths))
    return cliques[index_largest]


def heuristica_clique_con_mayor_suma(M, datos_prendas):
    cliques = finds_cliques(M)
    sumas = []
    for clique in cliques:
        suma = 0
        for x in clique:
            suma += datos_prendas[x]
        sumas.append(suma)
    index_max = sumas.index(max(sumas))
    return cliques[index_max]

def heuristica_clique_con_lavado_mas_largo(M, datos_prendas):
    cliques = finds_cliques(M)
    valores_maximos = []
    for clique in cliques:
        valores = []
        for x in clique:
            valores.append(datos_prendas[x])
        valores_maximos.append(max(valores))
    index_max = valores_maximos.index(max(valores_maximos))
    return cliques[index_max]

def heuristica_clique_con_suma_mas_grande_entre_los_mas_largos(M, datos_prendas):
    
    cliques = finds_cliques(M)
    
    lengths = []
    for clique in cliques:
        lengths.append(len(clique))
    max_length = max(lengths)

    largest_cliques = []
    for clique in cliques:
        if(len(clique) == max_length):
            largest_cliques.append(clique)
    
    sumas = []
    for clique in largest_cliques:
        suma = 0
        for x in clique:
            suma += datos_prendas[x]
        sumas.append(suma)
    
    index_max = sumas.index(max(sumas))

    return largest_cliques[index_max]

def heuristica_clique_mas_largo_entre_la_sumas_mas_grandes(M, datos_prendas):
    cliques = finds_cliques(M)
    sumas = []
    for clique in cliques:
        suma = 0
        for x in clique:
            suma += datos_prendas[x]
        sumas.append(suma)
    max_sum = max(sumas)
    max_indexes = []
    for i in range(len(sumas)):
        if (sumas[i] == max_sum):
            max_indexes.append(i)
    
    lengths = []
    for j in range(len(max_indexes)):
        lengths.append(len(cliques[j]))
    index_max = max_indexes[lengths.index(max(lengths))]
    return cliques[index_max]
# Funciones de resolucion y generacion de archivo

def resolver(incompatibilidades, datos_prendas, get_clique):
    M = matriz_de_compatibilidades(incompatibilidades)
    res = []
    prendas_a_lavar = set(M.keys())
    while(len(prendas_a_lavar) != 0):
        clique = get_clique(M, datos_prendas)
        res.append(clique)
        M = drop_vertices(M, clique)

        prendas_a_lavar = prendas_a_lavar.difference(set(clique))
    return res

def generate_result(res, nombre_archivo):
    content = ""
    i = 1
    for t in res:
        for e in t:
            content += str(e) + " " + str(i) + "\n"
        i += 1

    with open(nombre_archivo, 'w') as file:
        file.write(content)

# Funcion obtener puntaje:

def get_score(result, datos_prendas):
    tiempos_prendas = []
    for i in range(len(result)):
        tiempo = []
        for j in range(len(result[i])):
            tiempo.append(datos_prendas[result[i][j]])
        tiempos_prendas.append(tiempo)
    
    score = 0
    for t in tiempos_prendas:
        score += max(t)
    return score

# Funcion principal:

def main(nombre_archivo):
    incompatibilidades, datos_prendas = parsear_archivo(nombre_archivo)

    heuristicas = [
        [heuristica_clique_con_mayor_suma, "heuristica_clique_con_mayor_suma"],
        [heuristica_clique_mas_ahorro, "heuristica_clique_mas_ahorro"],
        [heuristica_clique_mas_largo_entre_la_sumas_mas_grandes, "heuristica_clique_mas_largo_entre_la_sumas_mas_grandes"],
        [heuristica_clique_con_suma_mas_grande_entre_los_mas_largos, "heuristica_clique_con_suma_mas_grande_entre_los_mas_largos"],
        [heuristica_clique_mas_largo, "heuristica_clique_mas_largo"],
        [heuristica_clique_con_lavado_mas_largo, "heuristica_clique_con_lavado_mas_largo"],
    ]

    for heuristica, nombre in heuristicas:
        res = resolver(incompatibilidades, datos_prendas, heuristica)
        generate_result(res, "outputs/e2_" + nombre + ".txt")
        print(nombre + ": ", get_score(res, datos_prendas))

main("inputs/segundo_problema.txt")
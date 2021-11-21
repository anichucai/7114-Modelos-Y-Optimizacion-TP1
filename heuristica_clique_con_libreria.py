import networkx
import networkx.algorithms.clique as clique

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
def resolver(incompatibilidades, datos_prendas):

    M = matriz_de_compatibilidades(incompatibilidades)

    # Clique
    G = networkx.Graph()

    for n_i in M.keys():
        for n_j in M[n_i]:
            G.add_node(n_i, weight=datos_prendas[n_i])
            G.add_node(n_j, weight=datos_prendas[n_j])


    for n_i in M.keys():
        for n_j in M[n_i]:
            G.add_edge(n_i, n_j)

    res = []
    while(len(G.nodes()) != 0):
        lavado = clique.max_weight_clique(G)[0]
        print(lavado)
        for n in lavado:
            G.remove_node(n)
        res.append(list(lavado))

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
    nombre = "clique_con_libreria"
    res = resolver(incompatibilidades, datos_prendas)
    generate_result(res, "outputs/e2_" + nombre + ".txt")
    print(nombre + ": ", get_score(res, datos_prendas))

main("inputs/segundo_problema.txt")
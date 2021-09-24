'''
HEURÍSTICA: Lavar aquellos conjutnos de prendas compatibles con aquellos lavados más largos inclusive.
'''

def parse_file(nombre_archivo):
    with open(nombre_archivo) as file:  
        data = [line.split() for line in file.readlines()]
    incompatibilidades = []
    tiempos_prendas = dict()
    n = 0
    for i in range(len(data)):
        if (data[i][0] == 'e'):
            incompatibilidades.append(data[i][1:])
        elif (data[i][0] == 'n'):
            tiempos_prendas[data[i][1]] = data[i][2]
        elif (data[i][0] == 'p'):
            n = int(data[i][2])
    return n, incompatibilidades, tiempos_prendas

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

def resolucion():
    n, incompatibilidades, datos_prendas = parse_file("primer_problema.txt")
    m_de_incompatibilidades = matriz_de_incompatibilidades(incompatibilidades)
    prendas_a_lavar = set(m_de_incompatibilidades.keys())
    prendas_lavadas = set()
    res = {}
    nro_lavado = 1
    costo = 0
    while(len(prendas_a_lavar) != 0):
        prenda_mas_pesada = max(prendas_a_lavar)
        costo += prenda_mas_pesada
        prendas_nuevo_lavado = prendas_a_lavar.difference(m_de_incompatibilidades[prenda_mas_pesada])
        for prenda in prendas_nuevo_lavado:
            res[prenda] = nro_lavado
        nro_lavado += 1
        prendas_lavadas.union(prendas_nuevo_lavado)
        prendas_a_lavar = prendas_a_lavar.difference(prendas_nuevo_lavado)
    return costo, res

def generate_result(res):
    content = ""
    for key in res.keys():
        content += str(key) + " " + str(res[key]) + "\n"
    with open('resultados/heuristica_1.txt', 'w') as file:
        file.write(content)

def main():
    costo, res = resolucion()
    generate_result(res)
    print("COSTO:", costo)
    print("LAVADOS:", res)

main()
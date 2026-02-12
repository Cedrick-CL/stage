import networkx as nx

def dotToData(file):
    G = nx.nx_pydot.read_dot(file)  

    data = []

    for u, v in G.edges():
        data.append(([val for val in u], [val for val in v]))

    return data

def compGraphe(file1, file2):
    G1 = nx.nx_pydot.read_dot(file1)  
    G2 = nx.nx_pydot.read_dot(file2)  
    
    print(f"Arêtes présentes que dans {file1} :")
    for arr in G1.edges():
        if arr not in G2.edges():
            print(f"{arr[0]} -> {arr[1]}")
    
    print(f"\nArêtes présentes que dans {file2} :")
    for arr in G2.edges():
        if arr not in G1.edges():
            print(f"{arr[0]} -> {arr[1]}")
            
compGraphe("Exemples/exMultiVal/graphe/sbml.dot", "Exemples/exMultiVal/graphe/ginml.dot")
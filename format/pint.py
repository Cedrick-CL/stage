import pylfit

data = [ \
(["0","0","0"],["0","0","1"]), \
(["1","0","0"],["0","0","0"]), \
(["0","1","0"],["1","0","1"]), \
(["0","0","1"],["0","0","1"]), \
(["1","1","0"],["1","0","0"]), \
(["1","0","1"],["0","1","0"]), \
(["0","1","1"],["1","0","1"]), \
(["1","1","1"],["1","1","0"])]

dataset = pylfit.preprocessing.discrete_state_transitions_dataset_from_array(data=data, feature_names=["p_t_1","q_t_1","r_t_1"], target_names=["p_t","q_t","r_t"])

model = pylfit.models.DMVLP(features=dataset.features, targets=dataset.targets)
model.compile(algorithm="pride") 

model.fit(dataset=dataset)

def modelToPint(model, outputName = "./pintfile"):
    with open(f"{outputName}.an", "w") as f:
        for features in model.features:
            f.write(f'"{features[0][:-4]}" {features[1]}\n')
        f.write("\n")
        
        for rules in model.rules:
            headVariable = rules.head.variable[:-2]
            bodyValues = rules.body.values()
            lenBodyValues = len(bodyValues)
            listBodyValues = list(bodyValues)
            bodyVariables = [values.variable[:-4] for values in bodyValues]
            
            if headVariable not in bodyVariables:
                etats = model.features[[model.features[i][0][:-4] for i in range(len(model.features))].index(headVariable)][1]
                for etat in etats:
                    if (etat != rules.head.value):
                        f.write(f'"{rules.head.variable[:-2]}" "{etat}" -> "{rules.head.value}"')
                        for condition in range(lenBodyValues):
                            if condition == 0:
                                f.write(f' when "{listBodyValues[condition].variable[:-4]}"="{listBodyValues[condition].value}"')
                            else: 
                                f.write(f'"{listBodyValues[condition].variable[:-4]}"="{listBodyValues[condition].value}"')
                            if condition < lenBodyValues - 1:
                                f.write(" and ")
                        f.write("\n")    
            
            else:
                nextValue = rules.body[rules.head.variable+"_1"].value 
                if nextValue != rules.head.value:
                    if lenBodyValues == 1:
                        f.write(f'"{rules.head.variable[:-2]}" "{nextValue}" -> "{rules.head.value}"\n')
                    else:
                        f.write(f'"{rules.head.variable[:-2]}" "{nextValue}" -> "{rules.head.value}"')
                        for condition in range(lenBodyValues):
                            currentVar = listBodyValues[condition].variable[:-4]
                            if (currentVar != headVariable):
                                if condition == 0:
                                    f.write(f' when "{listBodyValues[condition].variable[:-4]}"="{listBodyValues[condition].value}"')
                                else:
                                    f.write(f'"{listBodyValues[condition].variable[:-4]}"="{listBodyValues[condition].value}"')
                                if condition < lenBodyValues - 1:
                                    f.write(" and ")
                        f.write("\n")

                
modelToPint(model)

import networkx as nx
import matplotlib.pyplot as plt
import itertools

def visualize_model_graph(model, feature_names):
    # 1. Créer le graphe orienté
    G = nx.DiGraph()
    
    # 2. Générer tous les états possibles (000, 001, ..., 111)
    # On suppose que tes variables sont binaires (0 ou 1)
    nb_vars = len(feature_names)
    all_states = [list(s) for s in itertools.product(["0", "1"], repeat=nb_vars)]
    
    # 3. Pour chaque état, demander la prédiction au modèle
    for state in all_states:
        state_tuple = tuple(state)
        # On utilise la sémantique asynchrone pour voir toutes les transitions possibles
        predictions = model.predict([state], semantics="asynchronous")
        
        # Le format de retour est dict[tuple_etat_initial][tuple_etat_suivant]
        if state_tuple in predictions:
            for next_state_tuple in predictions[state_tuple]:
                u = "".join(state)
                v = "".join(next_state_tuple)
                G.add_edge(u, v)
    
    # 4. Dessiner le graphe
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42) # Positionnement des nœuds
    nx.draw(G, pos, with_labels=True, 
            node_color='skyblue', 
            node_size=2000, 
            edge_color='gray', 
            arrows=True, 
            arrowsize=20,
            font_weight='bold')
    
    plt.title("Graphe des transitions d'états (LFIT)")
    plt.show()

# Utilisation
visualize_model_graph(model, ["p", "q", "r"])



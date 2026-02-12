def modelToPint(model, outputName = "pint"):
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
                        nbrCond = 0
                        for condition in range(lenBodyValues):
                            if nbrCond == 0:
                                f.write(f' when "{listBodyValues[condition].variable[:-4]}"="{listBodyValues[condition].value}"')
                                nbrCond += 1
                            else: 
                                f.write(f' and "{listBodyValues[condition].variable[:-4]}"="{listBodyValues[condition].value}"')
                        f.write("\n")    
            
            else:
                nextValue = rules.body[rules.head.variable+"_1"].value 
                if nextValue != rules.head.value:
                    if lenBodyValues == 1:
                        f.write(f'"{rules.head.variable[:-2]}" "{nextValue}" -> "{rules.head.value}"\n')
                    else:
                        f.write(f'"{rules.head.variable[:-2]}" "{nextValue}" -> "{rules.head.value}"')
                        nbrCond = 0
                        for condition in range(lenBodyValues):
                            currentVar = listBodyValues[condition].variable[:-4]
                            if (currentVar != headVariable):
                                if nbrCond == 0:
                                    f.write(f' when "{listBodyValues[condition].variable[:-4]}"="{listBodyValues[condition].value}"')
                                    nbrCond += 1
                                else:
                                    f.write(f' and "{listBodyValues[condition].variable[:-4]}"="{listBodyValues[condition].value}"')
                        f.write("\n")

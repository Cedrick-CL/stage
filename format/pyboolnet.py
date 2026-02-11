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
model.summary()


def modelToPyboolnet(model, outputFile = "./output"):
    variable = [i[0][:-2] for i in  model.targets]
    rules = model.rules
    with open(f"{outputFile}.bnet", "w") as f:
        for var in variable: 
            countOrRules = 0
            f.write(f"{var}, ")
            for rule in rules:
                countAndRules = 0
                if rule.head.variable[:-2] == var and rule.head.value == "1":
                    listBody = list(rule.body.values())
                    lenBody = len(listBody)
                    if countOrRules != 0:
                        f.write(" | ")
                    if lenBody > 1:
                        f.write("(")
                    for condition in listBody:
                        if countAndRules != 0:
                            f.write(" & ")
                        if condition.value == "0":
                            f.write(f"!{condition.variable[:-4]}")
                        else:
                            f.write(f"{condition.variable[:-4]}")
                        countAndRules += 1
                    if lenBody > 1:
                        f.write(")")
                    countOrRules += 1
                #elif rule.head.variable[:-2] != var:
                    #break
            if countOrRules == 0:
                f.write("1")
            f.write("\n")

modelToPyboolnet(model)
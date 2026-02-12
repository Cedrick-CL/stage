# exemple provenant de https://ginsim.github.io/models/1995-lambda-lysis-lysogeny/
import pylfit
import networkx as nx
import readGraphe
import pint
import pyboolnet
import SBMLquad
import ginml


data = readGraphe.dotToData("Exemples\exMultiVal\multiVal.dot")

dataset = pylfit.preprocessing.discrete_state_transitions_dataset_from_array(data=data, feature_names=["p_t_1","q_t_1","r_t_1","s_t_1"], target_names=["p_t","q_t","r_t","s_t"])

model = pylfit.models.DMVLP(features=dataset.features, targets=dataset.targets)
model.compile(algorithm="pride") # model.compile(algorithm="gula")

model.fit(dataset=dataset)

pint.modelToPint(model, "exMultiVal")
ginml.modelToGinml(model, "exMultiVal")
SBMLquad.modelToSbmlQual(model, "exMultiVal")
pyboolnet.modelToPyboolnet(model, "exMultiVal")


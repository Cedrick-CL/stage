import libsbml
import pylfit

def formuleLogic(model, var0):
    rules = model.rules
    orClauses = []

    for rule in rules:
        if rule.head.variable[:-2] == var0 and rule.head.value == "1":
            andConditions = []
            for condition in rule.body.values():
                var = condition.variable[:-4]
                if condition.value == "0":
                    andConditions.append(f"!{var}")
                else:
                    andConditions.append(var)
            
            clause = "(" + " && ".join(andConditions) + ")"
            orClauses.append(clause)

    if not orClauses:
        return "0"
    
    return " || ".join(orClauses)

def modelToSbmlQual(model, outputFile="./output_model.sbml"):
    doc = libsbml.SBMLDocument(3, 1)
    doc.enablePackage("http://www.sbml.org/sbml/level3/version1/qual/version1", "qual", True)

    model_sbml = doc.createModel()
    qmodel = model_sbml.getPlugin("qual")

    variables_info = [(i[0][:-4], i[1][-1]) for i in model.features]
    for name, max_val in variables_info:
        qs = qmodel.createQualitativeSpecies()
        qs.setId(name)
        qs.setConstant(False)
        qs.setMaxLevel(int(max_val))

    for name, _ in variables_info:
        transition = qmodel.createTransition()
        
        output = transition.createOutput()
        output.setQualitativeSpecies(name)
        output.setTransitionEffect(libsbml.OUTPUT_TRANSITION_EFFECT_ASSIGNMENT_LEVEL)

        logic_str = formuleLogic(model, name)
        print(logic_str)

        for input_name, _ in variables_info:
            if input_name in logic_str and input_name != name:
                input_obj = transition.createInput()
                input_obj.setQualitativeSpecies(input_name)
                input_obj.setTransitionEffect(libsbml.INPUT_TRANSITION_EFFECT_NONE)

        ast_node = libsbml.parseL3Formula(logic_str)
        ft = transition.createFunctionTerm()
        ft.setResultLevel(1) 
        ft.setMath(ast_node)
        
        default_term = transition.createDefaultTerm()
        default_term.setResultLevel(0)

    libsbml.writeSBMLToFile(doc, outputFile)

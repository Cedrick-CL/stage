from random import randint

def modelToGinml(model, outputFile = "ginml"):
    variablesAndMax = [(i[0][:-4], i[1][-1]) for i in model.features]
    variables = [i[0] for i in variablesAndMax]
    rules = model.rules
    text = {}
    value = {}

    with open(f"{outputFile}.ginml", 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<!DOCTYPE gxl SYSTEM "http://ginsim.org/GINML_2_2.dtd">\n<gxl xmlns:xlink="http://www.w3.org/1999/xlink">\n')
        f.write(f'\t<graph id="phage4" class="regulatory" nodeorder="{" ".join(variables)}">\n')
        f.write(f'\t\t<nodestyle background="#ffffff" foreground="#000000" text="#000000" shape="RECTANGLE" width="45" height="25" properties="intermediate:#ffff00 active:#ffc800"/>\n\t\t<edgestyle color="#000000" pattern="SIMPLE" line_width="1" properties="positive:#00c800 negative:#c80000 dual:#0000c8"/>\n\n')
        for var in variablesAndMax:
            text[var[0]] = f'\t\t<node id="{var[0]}" maxvalue="{var[1]}">\n'
        
        edge = ""
        for var in variables: 
            put = False
            value[var] = '\t\t\t<value val="1">\n'
            for rule in rules:
                if rule.head.variable[:-2] == var and rule.head.value == "1":
                    
                    listBody = list(rule.body.values())
                    lenBody = len(listBody)
                    name = ""
                    for condition in listBody:
                        if condition.value == "0":
                            edge += f'\t\t<edge id="{var}:{condition.variable[:-4]}" from="{var}" to="{condition.variable[:-4]}" sign="negative">\n\t\t\t<edgevisualsetting anchor="NE" style=""/>\n\t\t</edge>\n'
                            if name == "":
                                name = f'\t\t\t\t<exp str="!{condition.variable[:-4]}'
                            else:
                                name += f' &amp !{condition.variable[:-4]}'
                                put = True
                        else:
                            if f'from="{var}" to="{condition.variable[:-4]}" sign="positive"' not in edge:
                                edge += f'\t\t<edge id="{var}:{condition.variable[:-4]}" from="{var}" to="{condition.variable[:-4]}" sign="positive">\n\t\t\t<edgevisualsetting anchor="NE" style=""/>\n\t\t</edge>\n'
                            if name == "":
                                name = f'\t\t\t\t<exp str="{condition.variable[:-4]}'
                            else:
                                name += f' &amp; {condition.variable[:-4]}'
                                put = True
                        if f'{var}:{condition.variable[:-4]}' not in text[var]:
                            text[var] += f'\t\t\t<parameter idActiveInteractions=" {var}:{condition.variable[:-4]}" val="1"/>\n' 
                    name += f'"/>\n'
                    value[var] += name
            if put:
                value[var] += '\t\t\t</value>\n'
                text[var] += value[var] 
            
        
        for node in list(text.values()):
            f.write(f'{node}\t\t\t<nodevisualsetting x="{randint(100,600)}" y="{randint(100,600)}" style=""/>\n\t\t</node>\n\n')
        
        f.write(f'{edge}\n\t</graph>\n</gxl>')


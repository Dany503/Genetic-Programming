import operator
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

# esta función es para realizar una división entre 0 de forma segura. No hace falta tocarla
def safeDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 0

# Estos a1, a2, a3 los tienes que recibir de NS-2
def new_metric(a1, a2, a3):
	f= open("new_metric.txt",'r')
	for line in f:
		individual = line

	func = toolbox.compile(expr=individual)
	inputs = [None] * 3
	
	inputs[0] = float(a1)
	inputs[1] = float(a2)
	inputs[2] = float(a3)

	metric = func(*inputs)
	if metric > 1:
		metric = -1
	if metric < 0:
		metric = -1
	return metric

# Aqui lo que hago es definir las funciones que estan permitidas en el arbol. Las tenemos que definir aqui por las usa el metodo toolbox.compile de la funcion new_metric de arriba 
pset = gp.PrimitiveSet("MAIN", 3,"input")
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(safeDiv, 2)
pset.addPrimitive(operator.neg, 1)
toolbox = base.Toolbox()
toolbox.register("compile", gp.compile, pset=pset)
a1 = 2 # esto lo he puesto aqui para probar, puedes variar estos valores para que vea que todo esta correcto
a2 = 5
a3 = 5

resultado = new_metric(a1, a2, a3)
print resultado # aqui tendrias que devolver el resultado a NS-2 para que lo utilice 

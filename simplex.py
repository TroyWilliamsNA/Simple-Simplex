import numpy as np

class LP:
	def __init__(lp,c,dir):
		'''mxn arr, 1x(n-1) array'''
		lp.c = c
		lp.rules = []
		lp.var = 0
		lp.constraints = 0
		lp.dir = dir
	
	
	def add_constraint(lp, vars, comp, limit):
		'''''''''''''''
		var is 1xn array,
		comp is "<=" "=" ">="
		limit is a float
		'''''''''''''''
		if (vars.shape[0] <= lp.var):
			# pad the entry so it has values for every variable
			vars = np.pad(vars, (0,lp.var - vars.shape[0]),
			"constant", constant_values=(0,0))
		else:
			# pad all other rules and objective function to include all vars
			lp.var = vars.shape[0]
			lp.c = np.pad(lp.c, (0,lp.var - lp.c.shape[0]), 
			"constant", constant_values=(0,0))
			for rule in lp.rules:
				rule[0] = np.pad(rule[0], (0,lp.var - rule[0].shape[0]),
				"constant", constant_values=(0,0))
		lp.rules.append([vars,comp,limit])
		
	
	def set_objective(lp,objective):
		'''objective is 1x(n-1) arr'''
		lp.c = np.transpose(objective)
		
	def set_constraints(lp,rules):
		'''objective is 1x(n-1) arr'''
		lp.rules = rules

	def print_lp(lp):
		print(lp.c, end='')
		print(lp.dir)
		for rule in lp.rules:
			print(rule[0], end='')
			print(rule[1], end='')
			print(rule[2])
			
	def copy(lp):
		cp = LP(lp.c.copy(),"max")
		cp.set_constraints(lp.rules.copy())
		return cp


def Standardize(lp):
	return lp.copy()




def Auxillerize(lp):
	print("Constructing Auxillary Problem")
	aux_var = 0
	aux = []
	for rule in lp.rules:
		aux.append(rule[0])
	aux = np.array(aux)
	print(aux)
	
	


print("Staring Operation Simplex")

test = LP(np.array([2,3,1,4,5]),"max")
test.add_constraint(np.array([1,1,1,0,2]),"<=",300)
test.add_constraint(np.array([1,0,1,2]),"<=",400)
test.add_constraint(np.array([1,0,1,2,3,4]),"<=",400)
test.print_lp()

'''
test2 = test.copy()
test2.print_lp()
test.add_constraint(np.array([1,0,1,2,3,4]),"<=",400)
test2.print_lp()
'''

Auxillerize(test)
import numpy as np
import copy as cp

np.set_printoptions(sign=' ',precision = 2)

''' For this LP all variables are strictly positive. '''
''' For free variables duplicate the column and negate it '''

class LP:
	def __init__(lp,c,dir):
		# c is a vector
		# dir is "max" or "min" '''
		lp.c = c
		lp.rules = []
		lp.var = c.shape[0]
		lp.constraints = 0
		lp.dir = dir
	
	
	def add_constraint(lp, vars, comp, limit):		
		#comp is "<=" "=" ">="
		#limit is a float		
		lp.constraints += 1
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

	def print_lp(lp):
		print(lp.c, end='')
		print(lp.dir)
		for rule in lp.rules:
			print(rule[0], end='')
			print(rule[1], end='')
			print(rule[2])
			
	def copy(lp):
		return cp.deepcopy(lp)
	

def Simplex(lp):
	basis = []
	lbls = []
	tableau = []
	av = 1
	sv = 1
	''' Set line 1 to the augmented objective
	    and line 2 to the original objective '''
	tableau.append(np.zeros(lp.c.shape[0]))
	tableau.append(-1 * lp.c)
	''' Push constraints into the tableau '''
	for i in range(1,lp.var+1):
		lbls.append(['x',i,i])
	for idx, rule in enumerate(lp.rules):
		if (rule[2] < 0):
			rule[0] *= -1
			rule[2] *= -1
			if (rule[1] == "<="):
				rule[1] = ">="
			elif (rule[1] == ">="):
				rule[1] = "<="
		tableau.append(rule[0])
	''' add slack and auxillery variables '''
	tableau = np.array(tableau)
	for idx, rule in enumerate(lp.rules):
		if (rule[1] == "<="):
			lbls.append(['s',idx,sv])
			basis.append(['s',idx,sv])
			sv += 1
			tableau = np.c_[tableau, np.zeros(lp.constraints + 2)]
			tableau[idx+2][tableau.shape[1] - 1] = 1
			rule[1] = "="
		elif (rule[1] == ">="):
			
			lbls.append(['s',idx,sv])
			sv += 1
			tableau = np.c_[tableau, np.zeros(lp.constraints + 2)]
			tableau[idx+2][tableau.shape[1] - 1] = -1
			lbls.append(['a',idx,av])
			basis.append(['a',idx,av])
			av += 1
			tableau = np.c_[tableau, np.zeros(lp.constraints + 2)]
			tableau[idx+2][tableau.shape[1] - 1] = 1
			tableau[0][tableau.shape[1] - 1] = 1
			rule[1] = "="
		elif (rule[1] == "="):
			lbls.append(['a',idx,av])
			basis.append(['a',idx,av])
			tableau = np.c_[tableau, np.zeros(lp.constraints + 2)]
			tableau[idx+2][tableau.shape[1] - 1] = 1
			tableau[0][tableau.shape[1] - 1] = 1
			av += 1
			
	
	b = [0,0]
	for rule in lp.rules:
		b.append(rule[2])
	b = np.array(b)
	tableau = np.c_[tableau, b]
	
	if(av > 1):
		for idx, var in enumerate(lbls):
			if (var[0] == 'a'):
				tableau[0] -= tableau[var[1]+2]
		
		print(tableau)
		print(basis)
		
		pcol = pivot_col(tableau)
		prow = pivot_row(tableau,pcol)
		print(pcol)
		print(prow)
		basis[prow-2] = lbls[pcol]
		
		while((pcol != -1) & (prow != -1)):
			perform_pivot(pcol,prow,tableau)
			pcol = pivot_col(tableau)
			prow = pivot_row(tableau,pcol)
			basis[prow-2] = lbls[pcol]
		if (prow == -1):
			print("PROBLEM HAS NO OPTIMAL SOLUTION")
			print("Certificate: " , end='')
			print(basis)
			return basis
		if (pcol == -1):
			print("OPTIMAL BASIS FOUND FOR AUXILLERY PROBLEM")
			print("STARTING PHASE TWO")
			
	if (av == 1):
		print("AUXILLERY PROBLEM NOT REQUIRED")
		print("STARTING PHASE TWO")
		print("Starting Basis: " , end='')
		print(basis)
	print(basis)
	#print(lbls)
	#print(tableau)











''' Locates the column on which the tableau should pivot
    return -1 if the current basis is optimal '''	
def pivot_col(tableau):
	min_col = -1
	min_val = 1
	for idx, col in enumerate(tableau[0]):
		if ((col < 0) & (col < min_val) & (idx != tableau.shape[1] - 1)):
			min_col = idx
			min_val = col
	return min_col
	
''' Locates the row on which the tableau should pivot
    return -1 if the problem is unbounded '''	
def pivot_row(tableau,col):
	if (col == -1):
		return -2
	height = tableau.shape[0]
	length = tableau.shape[1]
	min_row = -1
	min_val = -1
	for row in range(2,height):
		if (tableau[row][col] != 0):
			if ((tableau[row][col] != 0) & (tableau[row][length - 1] / tableau[row][col] > 0) & (tableau[0][row] < min_val)):
				min_row = row
				min_val = tableau[row][length - 1] / tableau[row][col]
	return min_row



def perform_pivot(c,r,tblu):
	piv_row = cp.deepcopy(tblu[r])
	piv_row /= piv_row[c]
	for idx, row in enumerate(tblu):
		row -= (row[c] * piv_row)
	tblu[r] = piv_row
	
	








''' TESTING '''
print("Staring Operation Simplex")

test = LP(np.array([-2,3,1,4,5]),"max")
test.add_constraint(np.array([-1,1,1,0]),"<=",30)
test.add_constraint(np.array([-1,0,1,2]),"<=",-40)
test.add_constraint(np.array([-1,0,1,2,3]),"=",40)
test.add_constraint(np.array([5,0,5,5]),">=",50)
#test.print_lp()


test2 = LP(np.array([-1,2,3,1,1]),"max")
test2.add_constraint(np.array([0,1]),"<=",10)
test2.add_constraint(np.array([1,0]),"<=",10)
#test2.print_lp()

Simplex(test)
Simplex(test2)

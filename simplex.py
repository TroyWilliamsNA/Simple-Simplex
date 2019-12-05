import numpy as np


class LP:
	def __init__(lp, constraints, objective):
		'''nxm arr, 1xn array'''
		lp.Ab = constraints
		lp.c = objective
		
	def add_constraint(lp, constraint):
		'''constraint is 1xn arr'''
		if (constraint.shape[0] > lp.Ab.shape[0]):
			z = np.zeros((lp.Ab.shape[0],lp.Ab.shape[1] - constraint.shape[0]))
			lp.Ab = np.append(lp.Ab,z)
		lp.Ab = numpy.vstack([lp.Ab, constraint])
		
	def set_objective(lp,objective):
		'''objective is 1xn arr'''
		lp.c = objective


print("Staring Operation Simplex")
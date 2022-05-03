from classes.AbstractVehicle import *

class Vehicle(AbstractVehicle):
	
	def __init__(self,ID,v):
		AbstractVehicle.__init__(self,ID,v)

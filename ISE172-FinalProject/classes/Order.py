
from classes.AbstractOrder import AbstractOrder
class Order(AbstractOrder):
	
	def __init__(self, fromV, toV):
		AbstractOrder.__init__(self,fromV, toV)



	def __str__(self):
		return str(self.pick_up_location)+" -> "+ str(self.drop_off_location  )
#creating the outline for vehicle pick up and drop off



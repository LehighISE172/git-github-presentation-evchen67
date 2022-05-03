from classes.AbstractWorld import *
 
import sys
import pygame
import random
pygame.font.init()

class World(AbstractWorld):
	def __init__(self, graph):
		AbstractWorld.__init__(self, graph)
		# set-up pygame
		self.height = 600
		self.width = 800
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.black = (0,0,0)
		self.white = (255, 255, 255)
		self.clock = pygame.time.Clock()
		self.font  = pygame.font.SysFont('Arial', 30)
		self.custFont  = pygame.font.SysFont('Arial', 15)
		self.explanFont  = pygame.font.SysFont('Arial', 22)


	def runSimulation(self, fps=1, initialTime=0, finalTime=30*60):

		'''
		This will give you a list of ALL vehicles which are in the system
		'''
		vehicles = self.getInitialVehicleLocations()
		for i,t in enumerate(vehicles):
			print ("vehicle %d: %s"%(i, str(t)) ) # print initial vehicle locations
			
		'''
		initialize vehicle images, resize it and get list of vehicles and rects
		Also make list to hold vehicle previous node and next node and speed
		'''
		carRects = []
		carList = []
		carNodes = []
		for j, d in enumerate(vehicles):
			car = pygame.image.load("data/car%d.png"%(j)) # car 0 gets car0 picture, car 1 gets car1, etc.
			car = pygame.transform.scale(car, (20, 20))   
			carList.append(car)
			carRects.append(car.get_rect())
			carNodes.append([None, None, None, None, None, None, None, []]) # all None to initialize
		
		'''
		Set vehicle starting locations and add to list of carNodes
		'''	
		for j in range(0, len(carRects)):
			key = random.choice(list(self.graph.verticies))
			x, y = self.graph.vertDict[key]
			carRects[j].centerx = x
			carRects[j].centery = y
			cost = 0
			carNodes[j] = [0, key, None, None, None, None, None, cost, []] # list of data for each car
		'''
		We will run a simulation where "t" is the time index
		'''
		delay = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		for t in range(initialTime,finalTime):	
			print ("\n\n Time: %02d:%02d"%(t/60, t%60))
			# each minute we can get a few new orders
			# this will show the current time in the simulation
			text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (self.black), (self.white))
			textrect = text.get_rect()
			textrect.centerx = 100
			textrect.centery = 30
			for j in range(0, len(carRects)):
				cost += carNodes[j][7] # add cost of each car's travel to total
			costText = self.font.render("Total Cost: $%02d"%(cost), True, (self.black), (self.white))
			costTextRect = costText.get_rect()
			costTextRect.centerx = 650
			costTextRect.centery = 30
			temp1 = ''
			for j in range(0, 11): # half of the cars
				temp1 += "Car "+str(j)+": "+str(len(carNodes[j][8]))+", " # print customer total per car
			customer1Text = self.custFont.render(temp1, True, (self.black), (self.white))
			customer1TextRect = customer1Text.get_rect()
			customer1TextRect.centerx = 400
			customer1TextRect.centery = 560
			temp2 = ''
			for j in range(11, len(carRects)): # half of the cars
				if j == len(carRects)-1: # remove comma at end
					temp2 += "Car "+str(j)+": "+str(len(carNodes[j][8])) # print customer total per car
				else:
					temp2 += "Car "+str(j)+": "+str(len(carNodes[j][8]))+", "
			customer2Text = self.custFont.render(temp2, True, (self.black), (self.white))
			customer2TextRect = customer2Text.get_rect()
			customer2TextRect.centerx = 400
			customer2TextRect.centery = 580
			explanation = self.explanFont.render("Customers Per Car", True, (self.black), (self.white))
			explanationRect = explanation.get_rect()
			explanationRect.centerx = 120
			explanationRect.centery = 530
			self.screen.fill(self.white)
			self.screen.blit(text, textrect)
			self.screen.blit(costText, costTextRect)
			self.screen.blit(customer1Text, customer1TextRect)
			self.screen.blit(customer2Text, customer2TextRect)
			self.screen.blit(explanation, explanationRect)
			
			orders = self.getNewOrdersForGivenTime(t)
			cust = []
			for o in orders: # collect new orders each minute
				customer = o.pick_up_location, o.drop_off_location
				cust.append(customer)
			for z in range(0, len(carRects)):
				if carNodes[z][8] == [] or len(carNodes[z][8]) == 1: # add limit of 2 customers per car
					if len(cust) > 0:
						carNodes[z][8].append(cust.pop()) # assign customer to first available car
					
			##Plots Graph
			for v in self.graph.verticies:
				center = self.graph.vertDict[v]
				pygame.draw.circle(self.screen,(48, 69, 255),center,4)
			for edge in self.graph.edges:
				for x in range(0, len(self.graph.edges[edge][1])-1):
					pygame.draw.line(self.screen, (133, 94, 28), self.graph.edges[edge][1][x], self.graph.edges[edge][1][x+1], 2)
			
			##Move Vehicles to random nodes
			for j in range(0, len(carRects)):
				counter, prior, next, destination, path, time, speed, cost, order = carNodes[j]
				if order == []:
					continue
				if next == None and destination == None and path == None and time ==  None and speed == None and order != []:
					path = self.graph.shortestPath[prior, order[0][0]] # find path for each car's order
					next = path[1]
					destination = order[0][0]
					time = self.graph.get_time(prior, next)
					speed = self.graph.get_speed(prior, next, carRects[j], time)
					carRects[j] = carRects[j].move(speed)
					carNodes[j] = [counter, prior, next, destination, path, time, speed, cost + .585, order] # update values
				if len(path)-1 == counter: # if a car reaches its customer's destination, idle for 10 mins
					car = self.graph.idleCar(j)
					carList[j] = car
					delay[j] = delay[j] + 1
					if delay[j] < 600:
						continue
					else: # when idle ends, assign new destination
						delay[j] = 0
						if carNodes[j][8][0][0] == destination: # check if car still has an order
							newDest = carNodes[j][8][0][1]
						elif carNodes[j][8][0][1] == destination:
							delete = order.pop()
							carNodes[j] = [0, destination, None, None, None, None, None, cost, order]
							car = self.graph.movingCar(j)
							carList[j] = car
							continue
						path = self.graph.shortestPath[destination, newDest]
						carNodes[j] = [0, destination, None, newDest, path, None, None, cost, order]
						car = self.graph.movingCar(j)
						carList[j] = car
						continue
				if next == None or time == None or speed == None:
					next = carNodes[j][4][counter + 1]
					time = self.graph.get_time(prior, next)
					speed = self.graph.get_speed(prior, next, carRects[j], time)
					carRects[j] = carRects[j].move(speed)
					carNodes[j] = [counter, prior, next, destination, path, time, speed, cost + .585, order]
				else:
					time -= 1
					carNodes[j] = [counter, prior, next, destination, path, time, speed, cost + .585, order]
					if time == 0:
						xNext, yNext = self.graph.vertDict[next]
						carRects[j].centerx = xNext
						carRects[j].centery = yNext
						carNodes[j] = [counter + 1, next, None, destination, path, None, None, cost, order]
						continue
					carRects[j] = carRects[j].move(speed)
			'''
			Update Screen
			'''	
			for j in range(0, len(carRects)):
				self.screen.blit(carList[j], carRects[j])
			pygame.display.flip()
			pygame.display.update()	
			'''
			Exit Program
			'''
			for event in pygame.event.get():  # TODO: Make sure that if we close the program, or hit exit the simulation will finish
				if event.type == pygame.QUIT:  
					pygame.quit()
					sys.exit()
			self.clock.tick(fps) 
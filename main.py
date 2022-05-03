import os
import pickle 
from classes.World import World
from classes.Graph import Graph 

current_working_dir = os.getcwd()
print("Your current working directory is: %s"%current_working_dir)

FPS = 200  # how many frames / second we will use in the simulation

with open("./data/Lehigh.pickle",'rb') as f:
    V, E = pickle.load(f, encoding="latin1")

graph = Graph(V, E)  # we will use this Graph class
myWorld = World(graph) # we create a world
myWorld.runSimulation(FPS) # we run some small simulation 



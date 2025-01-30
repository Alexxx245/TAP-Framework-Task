from mcpi import minecraft as Minecraft
import threading

class AgentManager:
    """ Main class that acts like the Minecraft Agent Framework
        Contains a list of agents and methods to manage them """

    def __init__(self):
        self.agents = []

    def register(self, agent):
        """ Method to register an agent to the list """
        self.agents.append(agent)

    def start(self, agent_id):
        """ Method to start a specific agent registered """
        self.agents[agent_id].start()

    def start_all(self):
        """ Method to start all the agents registered """
        for agent in self.agents:
            agent.start()

    def stop(self, agent_id):
        """ Method to stop a specific agent registered """
        self.agents[agent_id].stop()
    
    def stop_all(self):
        """ Method to stop all agents registered """
        for agent in self.agents:
            agent.stop()

    def kill(self, agent_id):
        """ Method to stop the thread of a specific agent and remove it from the list """
        self.stop(agent_id)
        self.agents.remove(self.agents[agent_id])
    
    def kill_all(self):
        """ Method to stop all agents and remove them from the list """
        self.stop_all()
        self.agents.clear()


class SpecificAgent:
    """ Class that contains methods that will implement 
        the different created agents """

    def __init__(self, name):
        self.name = name
        self.currentActivity = False    #variable to indicate the actual state of the agent, 
                                        #-> False means that the agent is stopped so he can't perform,
                                        #-> True means that the agent will wait to do his perform by matching the phrase key on the Minecraft chat
        self.mc = Minecraft.Minecraft.create()

    def start(self):
        """ Method to start an agent that uses the start method of threading module"""
        self.currentActivity = True
        threading.Thread(target=self.run).start()   #start basically puts the agent activity on true and runs it with a thread calling the specific perform method

    def run(self):
        """ Method that will execute the agent's work through another Thread """
        while self.currentActivity:
            self.perform()

    def perform(self):
        """ Abstract method that every agent have to implement on their own way """

    def stop(self):
        """ Method to stop an agent """
        self.currentActivity = False    #stop basically puts the agent activity on false which means he can't perform until it starts again

    def postToChat(self, message):
        """ Method to enable the CommandLine Agent to post messages on Minecraft Chat """
        self.mc.postToChat(self.name + " :" + message)      #this method is exclusive for the CommandLineAgent which allows him to post messages on the Minecraft chat using his name

    def getMethods(self):
        """ Method to get the methods of the agent """
        """ Use of reflective programming"""
        return [method for method in dir(self) if callable(getattr(self, method)) and not method.startswith("__")]      #this method is for using reflective programming
                                                                                                                        #because it is required by the professor and basically 
                                                                                                                        #puts on the Minecraft chat the defined methods of each agent,
                                                                                                                        #in this case all agents have the same methods but anyways
